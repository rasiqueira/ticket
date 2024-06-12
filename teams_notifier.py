import pymsteams

def send_teams_notification(ticket):
    myTeamsMessage = pymsteams.connectorcard("https://azureobvious.webhook.office.com/webhookb2/ec20fe2b-7ab7-4984-a149-76963c394c5a@5d41076b-a692-4668-95b2-6f5a3376b537/IncomingWebhook/5282782f33b842a9ab5b2416256ed407/74856ccd-bfff-4e59-852e-7d5fb27dbaa2")
    myTeamsMessage.title("Novo Ticket Recebido")
    myTeamsMessage.text(f"Novo ticket criado por {ticket['user']}: {ticket['title']}\nDescrição: {ticket['description']}")
    myTeamsMessage.send()