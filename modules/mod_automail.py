import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..main import Main

class automail():
    def __init__(self):
        """
        
        """


    def run(user_cred, to, subject, msgraw, exam="-", note="0,0"):
        """
        Params:
            user_cred: dict = {"mail_email": "XXX", "mail_pword": "XXX"}
            to: list = ["email@mail.com", "mail1@mail.com"],
            subject: String
            msgraw: String
            
        ---optionals:----
            exam: String
            note: String

        Modul schickt eine automatische Mail.
        
        """

        Main._set_state("automail: Verschicke Mail '%s'" % subject)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = user_cred.get('mail_email')
        msg['To'] = ', '.join(to)

        part = MIMEText(msgraw, 'html')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587) 
        server.ehlo()
        server.starttls()
        try:
            server.login(user_cred.get("mail_email"), user_cred.get("mail_pword"))
        except Exception as ex:
            print("FIRST",ex)
            return
        try:
            server.sendmail(user_cred.get("mail_email"), to, msg.as_string())
        except Exception as ex:
            print("SECOND", ex)
            return
        print("Mail sent successful")
        server.quit()

if __name__ == '__main__':
    with open("email_template.html", "r", encoding='utf-8') as f:
            text= f.read()
    
    automail.run(
        {"mail_email": "xtract.fea@gmail.com", "mail_pword": r"iumixnesoznogdvr"},
        ["florian.zasada@gmail.com"],
        "New",
        text,
        "EXAM",
        "1.9")
