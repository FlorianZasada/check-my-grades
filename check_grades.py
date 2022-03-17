from email import message
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

import time
from prettytable import PrettyTable

import os

from modules.mod_automail import automail
from modules.mod_loading_bar import loading_bar
from boto.s3.connection import S3Connection
from datetime import datetime, timedelta


from exceptions import NoGradeFoundException, NoModuleFoundException
import firebase_admin
from firebase_admin import credentials, firestore


BOT_ID = "recfDz9mQYpPU99pu"
automated_restarts = -1

class grades():

    def __init__(self):
        # Credentials JSON
        cred = credentials.Certificate('bot_creds.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()
        
        
        now = datetime.now() + timedelta(hours=1)
        datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
        
        data = {"started" : datestring}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
        
        
    def send_heartbeat(self):
        # Sendet eine Heartbeat Message an die Datenbank
        now = datetime.now() + timedelta(hours=1)
        datestring =  now.strftime("%d.%m.%Y, %H:%M:%S") 
        
        data = {"last_state" : datestring}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
        

    def _set_state(self, message):
        # Speichert einen Status in der Datenbank für die App
        data = {"status" : message}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)

    def _set_restart(self, i):
        # Speichert die Restart Variabel in die Datenbank
        data = {"automated_restarts" : str(i)}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
    
    def main(self):
        """
            Es wird auf die chromedriver.exe zugegriffen. Diese muss zwingend im Root Ordner liegen.

        """

        # Erhöhe Restarts und füge der Datenbank hinzu
        global automated_restarts
        automated_restarts += 1
        self._set_restart(automated_restarts)


        try:
            options = webdriver.ChromeOptions()

            options.binary_location  = os.environ.get('GOOGLE_CHROME_PATH')
            options.add_argument('--headless')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument("--window-size=1920x1080")
            


            # Öffnen des Browsers sowie den Seiten
            self.driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), options=options)
            try:
                self.driver.get(os.environ['QIS_URL'])
                self._set_state("Open URL")
            except:
                self._set_state(":efs: URL konnte nicht geöffnet werden")
                raise Exception


            # Anmeldung auf QIS
            try:
                input_username = self.driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(os.environ['QIS_USER'])
                input_pw = self.driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(os.environ['QIS_PASSWORD'])
                weiter_btn = self.driver.find_element_by_xpath("""//*[@id="content"]/div/div/div[2]/form/div/div[2]/input""").click()
                self._set_state("Logged in into QIS")
            except:
                self._set_state(":efs: Anmeldung fehlgeschlagen")
                raise Exception
            

            # Navigieren in die Ordnerstruktur, wo die Noten drinstehen
            try:
                leistung_btn = self.driver.find_element_by_xpath("""//*[@id="navi-main"]/li[3]/a""").click()
                semester = self.driver.find_element_by_xpath("""//*[@id="content"]/form/ul/li/ul/li/ul/li[2]/a[1]""").click()
            except:
                self._set_state(":efs: Fehler bei Navigation in QIS")
                raise Exception
    
            # Funktionsaufruf (Keine Parameter notwendig (Dauerschleife in sich selbst))
            now = datetime.now()
            f = open("restart.txt", "a+")
            f.write(f"reboot - {now} - \n\n")
            f.close()
            self._set_state("Start continous check...")
        except Exception as ex:
            self._set_state(ex)
            return
        self.continous_check()


        
    def continous_check(self):
        """
            Funktion prüft, ob Aänderungen im HTML Code (also Noten geändert oder nicht). Danach wartet sie 180s (3min)
            Und ruft sich erneut auf.

        """
        try:
            # Sende Heartbeat
            self.send_heartbeat()

            if not os.path.exists("tmp.txt"):
                open("tmp.txt", 'w').close()

            clear = lambda: print("\033c")
            clear()

            # Souper wird konfiguriert
            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            root = self.soup.findAll("tr", {"class" : ["MP", "PL"]})
            self._set_state("Get all Data from page")

            # Tabelle wird erstellt um eine schönere Dokumentation in der CMD zu ermöglichen
            x = PrettyTable()
            x.field_names = ["Modul", "Note"]



            # Hier wird druch die Module iteriert
            counter = 1
            avg = 0
            for i in root:
                for _ in range(5):
                    examName = i.find("span", {"class" : "examName"}).getText()
                    if examName:
                        break
                    time.sleep(.5)
                else:
                    raise NoModuleFoundException

                for _ in range(5):
                    grade = i.find("td", {"class" : "grade collapsed"}).getText()
                    if grade:
                        break
                    time.sleep(.5)
                else:
                    raise NoGradeFoundException


                # Hinzufügen zur Tabelle
                a = x.add_row([examName, grade.strip()])

                # Prüft, ob für Modul immernoch kein Eintrag
                if grade.strip() != "-":
                    # tmp erzeugen
                    f = open("tmp.txt", "r+")
                    z = f.read()
                    if examName in z:
                        pass
                    else:
                        f.write(examName+"\n")
                        f.close()

                    grade_for_avg = grade.strip().replace(",", ".")
                    avg += float(grade_for_avg) / counter


                    if examName not in z:
                        print(examName +": Note = "+ grade.strip())
                        grade_with_dot_notation = grade.strip().replace(",", ".")
                        self.sendmail(examName, grade_with_dot_notation)
                        counter+=1
                    else:
                        counter+=1
                        continue
                else:
                    continue

            if str(avg) == "0" and os.stat("tmp.txt").st_size != 1:
                self._set_state(":efs: Duchschnitt stimmt nicht mit Tmp zusammen!")
                raise Exception("Duchschnitt stimmt nicht mit Tmp zusammen!")
            
            
            #self.send_heartbeat()
            # Tabelle wird geprintet    
            print(x)            

            print("Durchschnitt: ~ "+str(avg))
            
            # Warte 30 Sekunden
            self._set_state("Waiting 30 seconds...")
            print("\nWarte 30 Sekunden...") 
            loading_bar(50, 0.5)
            clear()

            # Aktualisiere das Fenster
            self.driver.refresh()
            time.sleep(3)
            
        except Exception as ex:
            self._set_state(":efs:")
            return


        self.continous_check()
            
    def sendmail(self, exam, note):
        self._set_state("! Sende Mail !")
        #self.send_heartbeat()
        user_credentials = {"email" : os.environ['NOTI_MAIL'], "password" : os.environ["NOTI_PASSWORD"]}
        to_mail = ["florian.zasada@gmail.com", "florian.zasada@telekom.de", "Peter.Prumbach@telekom.de", "mail@peterprumbach.de", "fabian.lauret@telekom.de", "fabian@lauret-home.de", "georg.zibell@telekom.de", "georg.zibell@icloud.com"]
        subject = f"{exam} - NOTE IST RAUS!!!"
        msg = f"""
        Hi Leute,
<br>ich bins, NotiRobi 2.0.
<br>
<br>Auch dieses Semester sitze ich mit meiner Blechkiste auf dem Stuhl und überwache das Notengeschehen.
<br>Wie ihr mich kennt, melde ich mich nur, wenn ich eine Änderung sehe.
<br>
<br>
<br>Und wie ihr euch denken könnt, habe ich eine Änderung festgestellt...
<br>
<br>            <h2 style="color:red;"><b>Die Note für '{exam}' ist raus!</b></h2>           
<br>
<br>Schaue jetzt ins <a href="https://qisserver.htwk-leipzig.de/qisserver">QIS-Portal</a> und berichte :) 
<br>
<br>
<br>Liebe Grüße,
<br>NotiRobi 2.0
"""
        automail(user_credentials, to_mail, subject, msg)

        note_str = note.replace(".", ",")

        an_privat = ["florian.zasada@gmail.com"]
        subject_privat = f"{note_str} in {exam}"
        msg_privat = f"""Für die Klausur
<br>
<br>    <b>{exam}</b> wurde eine <b>{note_str}</b> 
<br>
<br>eingetragen!"""

        automail(user_credentials, an_privat, subject_privat, msg_privat)
        
        
if __name__ == '__main__':
    main = grades()
    for _ in range(100):
        try:
            main.main()
        except:
            raise

