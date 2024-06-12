import streamlit as st
import pandas as pd
import os
from authenticator import authenticator, roles
from teams_notifier import send_teams_notification

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
    if not os.path.exists('data/tickets.csv'):
        tickets = pd.DataFrame(columns=['user', 'title', 'description', 'status', 'respondent', 'response'])
        tickets.to_csv('data/tickets.csv', index=False)
    return pd.read_csv('data/tickets.csv')

def save_tickets(tickets):
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
                    new_ticket = {'user': username, 'title': title, 'description': description, 'status': 'Aberto', 'respondent': '', 'response': ''}
                    tickets = load_tickets()
                    tickets = tickets.append(new_ticket, ignore_index=True)
                    save_tickets(tickets)
                    
                    # Notificação no Teams
                    send_teams_notification(new_ticket)
                    
                    st.success('Ticket criado com sucesso!')

        st.title('Meus Tickets')
        tickets = load_tickets()
        my_tickets = tickets[tickets['user'] == username]
        st.dataframe(my_tickets)

        if st.sidebar.checkbox('Reabrir Ticket'):
            st.subheader('Reabrir Ticket')
            ticket_id = st.number_input('ID do Ticket para Reabrir', min_value=0, max_value=len(tickets) - 1)
            if ticket_id in tickets.index:
                st.text_area('Descrição do Ticket', value=tickets.at[ticket_id, 'description'], key='reopen_description')
                if st.button('Reabrir Ticket'):
                    tickets.at[ticket_id, 'status'] = 'Aberto'
                    tickets.at[ticket_id, 'respondent'] = ''
                    tickets.at[ticket_id, 'description'] = st.session_state['reopen_description']
                    save_tickets(tickets)
                    st.success(f'Ticket {ticket_id} reaberto.')

    elif role == "responder":
        st.title('Tickets para Responder')
        tickets = load_tickets()
        status_filter = st.sidebar.selectbox('Filtrar por Status', ['Todos', 'Aberto', 'Respondido'])
        
        if status_filter != 'Todos':
            tickets = tickets[tickets['status'] == status_filter]
        
        st.dataframe(tickets)
        
        if st.sidebar.checkbox('Responder Ticket'):
            st.subheader('Responder Ticket')
            ticket_id = st.number_input('ID do Ticket', min_value=0, max_value=len(tickets) - 1)
            if ticket_id in tickets.index:
                response_text = st.text_area('Resposta')
                if st.button('Marcar como Respondido'):
                    tickets.at[ticket_id, 'status'] = 'Respondido'
                    tickets.at[ticket_id, 'respondent'] = username
                    tickets.at[ticket_id, 'response'] = response_text
                    save_tickets(tickets)
                    st.success(f'Ticket {ticket_id} marcado como respondido.')

elif authentication_status == False:
    st.error('Nome de usuário ou senha incorretos')

elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')


elif authentication_status == None:
    st.warning('Por favor, insira seu nome de usuário e senha')
