import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class automail():
    def __init__(self, user_cred, to, subject, msgraw):
        """
            user_cred : dict
            {'email' : 'xy@gmail.com', 'password': 'pw'}

            to : list
            ['xy@gmai.com', 'zebra@gmx.net']

            subject:  String

            msg : html-String
        
        """

        self.user_cred = user_cred
        self.to = to
        self.subject = subject
        self.msgraw = msgraw

        self.create_mail()


    def create_mail(self):
            # msg = MIMEText(msg)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = self.user_cred.get('email')
            msg['To'] = ', '.join(self.to)

            part = MIMEText(self.msgraw, 'html')
            msg.attach(part)

            server = smtplib.SMTP('smtp.gmail.com:587')
            server.ehlo()
            server.starttls()
            # server.ehlo()
            server.login(self.user_cred.get("email"), self.user_cred.get("password"))
            try:
                server.sendmail(self.user_cred.get("email"), self.to, msg.as_string())
                print ('email sent')
            except:
                print ('error sending mail')
            server.quit()

if __name__ == '__main__':
    automail({"email": "robot@florianzasada.com", "password": r"%Flomaluju15"}, "florian.zasada@gmail.com", "New", "<h1>HIIII</h1>")
