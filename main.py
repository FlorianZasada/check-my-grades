from email import message
from typing import final
from boto import config
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
import pytz
from prettytable import PrettyTable
import os
import sys
from modules.mod_automail import automail
from modules.mod_qis_login import qis_login
from modules.mod_navigation import navigation

from boto.s3.connection import S3Connection
from datetime import datetime, timedelta


from exceptions import NoGradeFoundException, NoModuleFoundException
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore
from firebase_admin import storage

# Import UUID4 to create token
from uuid import uuid4

from _localconfig import config


BOT_ID = "recfDz9mQYpPU99pu"


class Main():

    def __init__(self):
        # Credentials JSON
        cred = credentials.Certificate('/home/pi/bin/check-my-grades/bot_creds.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

        # Reset State
        self.send_heartbeat()
        self._set_state("")
        self._set_state("Starte...")
       

        # Konfiguriert aktuellen Timestamp
        tz = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz)
        datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
        self._set_state("starte Story")


        # Starte Story
        self.main()

    def send_heartbeat(self):
        # Sendet eine Heartbeat Message an die Datenbank
        tz = pytz.timezone('Europe/Berlin')
        now = datetime.now(tz)
        datestring =  now.strftime("%d.%m.%Y, %H:%M:%S") 
        
        data = {"last_state" : datestring, "runtime": "Aktiv"}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
        
    def _set_state(self, message):
        # Speichert einen Status in der Datenbank für die App
        data = {"status" : message}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
        
    def _set_log(self, message):
        data = {"log" : message}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)

    def main(self):
        """
            Es wird auf die chromedriver.exe zugegriffen. Diese muss zwingend im Root Ordner liegen.

        """
        self.send_heartbeat()


        try:
            opt = Options()
            opt.add_argument("--start-maximized")
            opt.add_argument("headless")
            opt.add_argument("disable-gpu")


            # Öffnen des Browsers sowie den Seiten
            self._set_state("Öffne driver")
            self.driver = webdriver.Chrome(options = opt, executable_path = config["chromedriver_path"])
            self._set_state("Driver registriert")

            try:
                self._set_state("Öffne QIS URL")
                self.driver.get(config["qis_url"])
                
            except:
                raise Exception("URL konnte nicht geöffnet werden")

            # Anmeldung auf QIS
            try:
                qis_login.run(self.driver, config["qis_uname"], config["qis_pword"])
                self._set_state("In QIS eingeloggt")
            except:
                raise Exception("Anmeldung fehlgeschlagen")
            

            # Navigieren in die Ordnerstruktur, wo die Noten drinstehen
            try:
                navigation.run(self.driver, "Sommersemester 2022")
                self._set_state("Ins Semester navigiert")
            except Exception as ex:
                raise Exception(ex, "Fehler bei Navigation in QIS")
    
            # Funktionsaufruf (Keine Parameter notwendig (Dauerschleife in sich selbst))
            self.continous_check()
        except Exception as ex:
            self.driver.close()
            self._set_state(":efs: "+ str(ex))
            return


        
    def continous_check(self):
        """
            Funktion prüft, ob Aänderungen im HTML-Dom (also Noten geändert oder nicht). Danach wartet sie 180s (3min)
            Und ruft sich erneut auf.

        """

        while True:
            try:
                # Sende Heartbeat
                self.send_heartbeat()

                if not os.path.exists("tmp.txt"):
                    open("tmp.txt", 'w').close()


                # Souper wird konfiguriert
                self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                root = self.soup.findAll("tr", {"class" : "MP"})


                # Tabelle wird erstellt um eine schönere Dokumentation in der CMD zu ermöglichen
                x = PrettyTable()
                x.field_names = ["Modul", "Note"]

                # Hier wird druch die Module iteriert
                counter = 1
                avg = 0
                avg_mid = 0
                for i in root:
                    try:
                        for _ in range(5):
                            examName = i.find("span", {"class" : "examName"}).getText()
                            if examName:
                                break
                            time.sleep(.5)
                        else:
                            raise NoModuleFoundException("No Module")
                    except NoModuleFoundException as ex:
                        raise ex

                    try: 
                        for _ in range(5):
                            try:
                                grade = i.find('td', {"class" : "grade collapsed"}).getText().strip()
                            except:
                                grade = i.find('td', {"class" : "grade"}).getText().strip()
                            
                            if grade == "5":
                                grade = "0"
                            if grade:
                                break
                            time.sleep(.5)
                        else:
                            raise NoGradeFoundException("No Grade")
                    except NoGradeFoundException as ex:
                        raise ex


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
                        avg_mid += float(grade_for_avg) 
                        avg = avg_mid / counter


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
                
                self.send_heartbeat()
                
                # Warte 30 Sekunden
                self._set_state("Warte 30 Sekunden...")
                self._set_log(x.get_string())


                # Aktualisiere das Fenster
                self.driver.refresh()
                time.sleep(3)
                
            except Exception as ex:
                self.driver.close()
                self._set_state(":efs: " + str(ex))
                return

            
    def sendmail(self, exam, note):
        self._set_state("! Sende Mail !")
        user_credentials = config["email_credentials"]
        to_mail = ["florian.zasada@gmail.com", "florian.zasada@telekom.de"]
        subject = f"{exam} - NOTE IST RAUS!!!"

        report_file = open('email_template.html')
        html = report_file.read()

        msg = html
        automail.run(user_credentials, to_mail, subject, msg, exam, note)


#         msg = f"""
#         Hi Leute,
# <br>ich bins, NotiRobi 2.0.
# <br>übrigens bin ich umgezogen...ich sitz mir jetzt mein Sitzstahl in einem Raspberry Pi wund ;D
# <br>
# <br>Auch dieses Semester überwache ich das Notengeschehen.
# <br>Wie ihr mich kennt, melde ich mich nur, wenn ich eine Änderung sehe.
# <br>
# <br>
# <br>Und wie ihr euch denken könnt, habe ich eine Änderung festgestellt...
# <br>
# <br>            <h2 style="color:red;"><b>Die Note für '{exam}' ist raus!</b></h2>           
# <br>
# <br>Schaue jetzt ins <a href="https://qisserver.htwk-leipzig.de/qisserver">QIS-Portal</a> und berichte :) 
# <br>
# <br>
# <br>Liebe Grüße,
# <br>NotiRobi 2.0
# """
        
        
if __name__ == '__main__':
    grades()