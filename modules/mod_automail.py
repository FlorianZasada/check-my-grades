import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..main import Main

class Automail():
    def __init__(self):
        """
        
        """

    def get_whole_table(self):
      return 

    def contructed_message(self, exam, grade, semester, prof, time, average, grade_list):
        return """
        
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Demystifying Email Design</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    
  </head>

  <body>
    <div class="container">
      <div class="row">
        <h1>Hallo Florian!</h1>
      </div>
      <div class="row" style="margin-bottom: 3rem">
        <h2>Es wurde eine neue Note eingetragen für</h2>
      </div>
        <br>
        <div class="row" style="margin-left: 30%; margin-right:30%; margin-bottom:2rem">
          <table class="table table-sm">
              <tr>
                <td>Modul :</td>
                <td>%s</td>
              </tr>
              <tr>
                <td>Note :</td>
                <td>%s</td>
              </tr>
              <tr>
                <td>Semester :</td>
                <td>%s</td>
              </tr>
              <tr>
                <td>Bearbeiter :</td>
                <td>%s</td>
              </tr>
              <tr>
                <td>Zeitstempel :</td>
                <td>%s</td>
              </tr>
            </table>
        </div>

        <div class="row" style="margin-bottom:10px;">
          <p style="width:100%; text-align:right; margin-left: auto;">Es fehlen nur noch 1 Note</p>
            <hr style="height: 2px; color: black" />
        </div>
          
        <hr style="margin-top: 10px; margin-bottom: 50px">

        <div class="row" style="margin-bottom: 20px">
          Somit sieht dein Notenspiegel für das 2. Semester aktuell so aus:
        </div>
            
        <div class="row" style="margin-left: 3%; margin-right:3%; margin-bottom:1rem">
       """ + self.construct_table(grade_list, average) + """
        </div>

            <div class="row" style="margin-bottom:3rem;"> 
              <p><a href="#">Hier </a> geht es zum QIS-Portal!</p>
            </div>


            <!-- Footer -->
            <div class="row" style="background-color: rgb(203, 203, 105);">
              <div class="col" style="padding: 20px">
                &reg; Someone, somewhere 2013<br />
                      Unsubscribe to this newsletter instantly
              </div>
              <div class="col" style="padding: 20px">
                <a href="#"> QIS Protal Sachsen - HTWK </a>
              </div>
            </div>
          </div>
    <style>
      .dot {
        height: 25px;
        width: 25px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
      }
    </style>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js" integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.14.7/dist/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
  </body>
</html>

        
        """ %(exam, grade, semester, prof, time)


    def construct_table(self, grade_list, average):
      table_string =  """<table class="table table-striped table-sm">
          <thead>
            <tr>
              <th style="border-bottom: solid rgb(50, 187, 255) 1px" width="260" valign="top">#</th>
              <th style="border-bottom: solid rgb(50, 187, 255) 1px" width="260" valign="top">Modul</th>
              <th style="border-bottom: solid rgb(50, 187, 255) 1px" width="260" valign="top">Note</th>
              <th style="border-bottom: solid rgb(50, 187, 255) 1px" width="260" valign="top">Zeit</th>
              <th style="border-bottom: solid rgb(50, 187, 255) 1px" width="260" valign="top">Status</th>
            </tr>
          </thead> """

      

      for row in grade_list:
        if row[2] == "5,0" or row[2] == "5.0":
          color = "#f00"
        elif row[2] == "-" or row[2] == "":
          color = "#bbb"
        else:
          color = "#0f0"
          

        table_string.append(f"""<tr>
          <td width="260" valign="center">{row[0]}</td>
          <td width="260" valign="center">{row[1]}</td>
          <td width="260" valign="center">{row[2]}</td>
          <td width="260" valign="center">{row[3]}</td>
          <td width="260" valign="center"><span style="height: 20px;
                                                        width: 20px;
                                                        background-color: {color};
                                                        border-radius: 50%;
                                                        display: inline-block;">
                                          </span>
          </td>
        </tr>""")




      table_string.append("""<tfoot>
            <tr>
              <td width="260" valign="center"></td>
              <td width="260" valign="center">Durchschnitt</td>
              <td width="260" valign="center">%d</td>
              <td width="260" valign="center"></td>
              <td width="260" valign="center"></td>

            </tr>
          </tfoot>
        </table>""" % (average)) 

      return table_string



    def run(self, user_cred, to, subject, prof, semester, average, time, grade_list, exam="-", grade="0,0"):
        """
        Params:
            user_cred: dict = {"mail_email": "XXX", "mail_pword": "XXX"}
            to: list = ["email@mail.com", "mail1@mail.com"],
            subject: String
            prof: String,
            average: Float
            time: String
            grade_list: list
            
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

        msgraw = self.contructed_message(exam, grade, semester, prof, time, average, grade_list)

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
    
    Automail.run(
        {"mail_email": "xtract.fea@gmail.com", "mail_pword": r"iumixnesoznogdvr"},
        ["florian.zasada@gmail.com"],
        "New",
        text,
        "EXAM",
        "1.9")
