import streamlit as st
import pandas as pd
import os
from authenticator import authenticator, roles
from teams_notifier import send_teams_notification
from datetime import datetime

# Inicializar o estado da sessão
if 'authentication_status' not in st.session_state:
    st.session_state['authentication_status'] = None
if 'name' not in st.session_state:
    st.session_state['name'] = ''
if 'username' not in st.session_state:
    st.session_state['username'] = ''
if 'logout' not in st.session_state:
    st.session_state['logout'] = False

# Função para carregar e salvar tickets
def load_tickets():
    if not os.path.exists('data'):
        os.makedirs('data')
    if not os.path.exists('data/tickets.csv'):
        tickets = pd.DataFrame(columns=['Usuário', 'Título', 'Descrição', 'Status', 'Respondente', 'Resposta', 'Data de Abertura', 'Data de Fechamento'])
        tickets.to_csv('data/tickets.csv', index=False)
    tickets = pd.read_csv('data/tickets.csv', parse_dates=['Data de Abertura', 'Data de Fechamento'])
    return tickets

def save_tickets(tickets):
    if not os.path.exists('data'):
        os.makedirs('data')
    tickets.to_csv('data/tickets.csv', index=False)

# Autenticação
name, authentication_status, username = authenticator.login()

if authentication_status:
    role = roles.get(username)
    st.sidebar.title(f'Bem-vindo, {name} ({role})')

    if role == "creator":
        if st.sidebar.checkbox('Criar Ticket'):
            st.title('Criar Novo Ticket')
            
            with st.form('ticket_form'):
                title = st.text_input('Título do Ticket')
                description = st.text_area('Descrição do Ticket')
                submitted = st.form_submit_button('Enviar')
                
                if submitted:
                    new_ticket = pd.DataFrame([{
                        'Usuário': username,
                        'Título': title,
                        'Descrição': description,
                        'Status': 'Aberto',
                        'Respondente': '',
                        'Resposta': '',
                        'Data de Abertura': datetime.now(),
                        'Data de Fechamento': pd.NaT
                    }])
                    tickets = load_tickets()
                    tickets = pd.concat([tickets, new_ticket], ignore_index=True)
                    save_tickets(tickets)
                    
                    # Notificação no Teams
                    send_teams_notification(new_ticket.to_dict(orient='records')[0])
                    
                    st.success('Ticket criado com sucesso!')

        st.title('Meus Tickets')
        tickets = load_tickets()
        my_tickets = tickets[tickets['Usuário'] == username]
        
        # Adicionar flag de status
        my_tickets['Status Flag'] = my_tickets['Status'].apply(lambda x: '🟢' if x == 'Respondido' else '🔴')
        
        st.dataframe(my_tickets[['Título', 'Descrição', 'Status', 'Respondente', 'Resposta', 'Data de Abertura', 'Data de Fechamento', 'Status Flag']])

        if st.sidebar.checkbox('Reabrir Ticket'):
            st.subheader('Reabrir Ticket')
            ticket_id = st.number_input('ID do Ticket para Reabrir', min_value=0, max_value=len(tickets) - 1)
            if ticket_id in tickets.index:
                st.text_area('Descrição do Ticket', value=tickets.at[ticket_id, 'Descrição'], key='reopen_description')
                if st.button('Reabrir Ticket'):
                    tickets.at[ticket_id, 'Status'] = 'Aberto'
                    tickets.at[ticket_id, 'Respondente'] = ''
                    tickets.at[ticket_id, 'Descrição'] = st.session_state['reopen_description']
                    tickets.at[ticket_id, 'Data de Fechamento'] = pd.NaT
                    save_tickets(tickets)
                    st.success(f'Ticket {ticket_id} reaberto.')

        # Filtro por status
        status_filter = st.selectbox('Filtrar por Status', ['Todos', 'Aberto', 'Respondido'])
        if status_filter != 'Todos':
            my_tickets = my_tickets[my_tickets['Status'] == status_filter]
        
        st.dataframe(my_tickets)

    elif role == "responder":
        st.title('Tickets para Responder')
        tickets = load_tickets()
        
        # Filtro por status
        status_filter = st.selectbox('Filtrar por Status', ['Todos', 'Aberto', 'Respondido'])
        if status_filter != 'Todos':
            tickets = tickets[tickets['Status'] == status_filter]
        
        # Adicionar flag de status
        tickets['Status Flag'] = tickets['Status'].apply(lambda x: '🟢' if x == 'Respondido' else '🔴')
        
        st.dataframe(tickets[['Título', 'Descrição', 'Status', 'Respondente', 'Resposta', 'Data de Abertura', 'Data de Fechamento', 'Status Flag']])
        
        if st.sidebar.checkbox('Responder Ticket'):
            st.subheader('Responder Ticket')
            ticket_id = st.number_input('ID do Ticket', min_value=0, max_value=len(tickets) - 1)
            if ticket_id in tickets.index:
                response_text = st.text_area('Resposta')
                if st.button('Marcar como Respondido'):
                    tickets.at[ticket_id, 'Status'] = 'Respondido'
                    tickets.at[ticket_id, 'Respondente'] = username
                    tickets.at[ticket_id, 'Resposta'] = response_text
                    tickets.at[ticket_id, 'Data de Fechamento'] = datetime.now()
                    save_tickets(tickets)
                    st.success(f'Ticket {ticket_id} marcado como respondido.')

elif authentication_status == False:
    st.error('Nome de usuário ou senha incorretos')

elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
