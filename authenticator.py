import streamlit_authenticator as stauth

# Definição de usuários e suas roles
users = [
    {"name": "Suzi", "username": "suzi", "password": "Obvious@2024", "role": "creator"},
    {"name": "Rodrigo", "username": "rodrigo", "password": "Obvious@2024", "role": "responder"}
]

names = [user["name"] for user in users]
usernames = [user["username"] for user in users]
passwords = [user["password"] for user in users]
roles = {user["username"]: user["role"] for user in users}

hashed_passwords = stauth.Hasher(passwords).generate()

# Estrutura de credenciais esperada
credentials = {
    "usernames": {
        user["username"]: {
            "name": user["name"],
            "password": hashed_password
        } for user, hashed_password in zip(users, hashed_passwords)
    }
}

authenticator = stauth.Authenticate(
    credentials,
    'ticket_system',
    'abcdef'
)