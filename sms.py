from twilio.rest import Client


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
def send_sms(number, message_format):
    account_sid = 'ACe5801a49fd2ce6841d31d048729c86e7'
    auth_token = '702b4dcd1f89a81e93bb078b39ccf80b'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
                         body=f"{message_format}",
                         from_='+18609575836',
                         to=f'+91{number}'
                     )

    print(message.sid)