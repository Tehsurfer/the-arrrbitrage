from twilio.rest import Client

Dimi = '+61402904441'
Jesse = '+642041258195'
Twilio_Phone = '+61438887249'


class texter:
    def __init__(self):
        self.account_sid = "****************"
        # Your Auth Token from twilio.com/console
        self.auth_token = "**********************"

    def send_text(self, text):
        # Your Account SID from twilio.com/console

        client = Client(self.account_sid, self.auth_token)

        message = client.messages.create(
            to=Dimi,
            from_=Twilio_Phone,
            body=text)

        print(message.sid)
