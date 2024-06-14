import requests

def send_teams_notification(ticket):
    url = "https://v5.chatpro.com.br/chatpro-ios4d25121/api/v1/send_message"
    
    payload = {
    "number": "120363294576816106@g.us",
    "message": f"Novo ticket criado por {ticket['user']}: {ticket['title']}\nDescrição: {ticket['description']}"
    }
    headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "99dabc5b3db541e244cf908d993ce068"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
