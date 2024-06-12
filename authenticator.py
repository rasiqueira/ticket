import streamlit as st
import streamlit_authenticator as stauth

# Acessar os segredos
credentials = st.secrets["credentials"]

names = [credentials["user1_name"], credentials["user2_name"]]
usernames = [credentials["user1_username"], credentials["user2_username"]]
passwords = [credentials["user1_password"], credentials["user2_password"]]
roles = {
    credentials["user1_username"]: credentials["user1_role"],
    credentials["user2_username"]: credentials["user2_role"]
}

# Estrutura de credenciais esperada
hashed_passwords = stauth.Hasher(passwords).generate()
credentials_dict = {
    "usernames": {
        usernames[i]: {
            "name": names[i],
            "password": hashed_passwords[i]
        } for i in range(len(usernames))
    }
}

authenticator = stauth.Authenticate(
    credentials_dict,
    'ticket_system',  # Este é o nome da aplicação
    'abcdef',  # Um segredo utilizado na geração dos cookies
    cookie_expiry_days=1
)
