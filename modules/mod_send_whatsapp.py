from twilio.rest import Client

class send_whatsapp():
    def __init__(self, message,  from_nr="+14155238886", to_nr="+4916098685260"):
        self.from_nr = from_nr
        self.to_nr = to_nr
        self.message = message

        # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
        client = Client()

        # this is the Twilio sandbox testing number
        from_whatsapp_number='whatsapp:'+ self.from_nr
        # replace this number with your own WhatsApp Messaging number
        to_whatsapp_number='whatsapp:' + self.to_nr

        client.messages.create(body=self.message,
                            from_=from_whatsapp_number,
                            to=to_whatsapp_number)

if __name__ == "__main__":
    send_whatsapp("+14155238886", "+4916098685260", "Hier steht die Message")