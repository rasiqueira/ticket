import streamlit_authenticator as stauth
import streamlit as st
import bcrypt

# Acessar os segredos
credentials = st.secrets["credentials"]

users = [
    {"name": credentials["user1_name"], "username": credentials["user1_username"], "password": credentials["user1_password"], "role": credentials["user1_role"]},
    {"name": credentials["user2_name"], "username": credentials["user2_username"], "password": credentials["user2_password"], "role": credentials["user2_role"]}
]

names = [user["name"] for user in users]
usernames = [user["username"] for user in users]
passwords = [user["password"] for user in users]
roles = {user["username"]: user["role"] for user in users}

# Gerar senhas hash usando bcrypt
hashed_passwords = [bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() for password in passwords]

# Estrutura de credenciais esperada
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
