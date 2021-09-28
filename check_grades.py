from email import message
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import time
from prettytable import PrettyTable

from selenium.webdriver.chrome.options import Options
import sys
import os

from modules.mod_automail import automail
from modules.mod_loading_bar import loading_bar
import re

from boto.s3.connection import S3Connection

from datetime import date, datetime

from exceptions import NoGradeFoundException, NoModuleFoundException

class grades():

    def __init__(self):
        # config_items = ["QIS_uname", "QIS_pword", "QIS_url", "notirobi_mail", "notirobi_pword"]
        # keys = []
        # self.config_item_dict = {}
        
        # f = open(r"C:\Windows\System32\cmd.exe\_localconfig.txt", "r")
        # for x in f:
        #     a = re.search('"(.*?)"', x).group(0).replace('\"', '')
        #     keys.append(a)

        # for i in range(len(config_items)):
        #     self.config_item_dict[config_items[i]] = keys[i]

        now = datetime.now()
        datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
        self.main()

    def main(self):
        """
            Es wird auf die chromedriver.exe zugegriffen. Diese muss zwingend im Root Ordner liegen.

        """

        GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
        CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.binary_location = GOOGLE_CHROME_PATH


        # Öffnen des Browsers sowie den Seiten
        url = os.environ['QIS_URL']
        # self.driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
        self.driver = webdriver.Chrome()
        self.driver.get(url)


        # Anmeldung auf QIS
        input_username = self.driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(os.environ['QIS_USER'])
        input_pw = self.driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(os.environ['QIS_PASSWORD'])
        weiter_btn = self.driver.find_element_by_xpath("""//*[@id="content"]/div/div/div[2]/form/div/div[2]/input""").click()

        # Navigieren in die Ordnerstruktur, wo die Noten drinstehen
        leistung_btn = self.driver.find_element_by_xpath("""//*[@id="main"]/div/div[2]/div[2]/a""").click()
        semester = self.driver.find_element_by_xpath("""//*[@id="content"]/form/ul/li/ul/li/ul/li[2]/a[1]""").click()


        # Funktionsaufruf (Keine Parameter notwendig (Dauerschleife in sich selbst))
        now = datetime.now()
        f = open("restart.txt", "a+")
        f.write(f"reboot - {now} - \n\n")
        f.close()
        self.continous_check()


        
    def continous_check(self):
        """
            Funktion prüft, ob Aänderungen im HTML Code (also Noten geändert oder nicht). Danach wartet sie 180s (3min)
            Und ruft sich erneut auf.

        """

        if not os.path.exists("tmp.txt"):
            open("tmp.txt", 'w').close()


        clear = lambda: os.system('cls')
        clear()

        # Souper wird konfiguriert
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        root = self.soup.findAll("tr", {"class" : ["MP", "PL"]})

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

        if str(avg) == "0" and os.stat("tmp.txt").st_size != 0:
            raise Exception("Kein Zugriff auf QIS!")
        
        # Tabelle wird geprintet    
        print(x)            

        print("Durchschnitt: ~ "+str(avg))
        
        # Warte 30 Sekunden
        print("\nWarte 30 Sekunden...") 
        loading_bar(50, 0.5)
        clear()

        # Aktualisiere das Fenster
        self.driver.refresh()
        time.sleep(3)
        
        #wiederholter Aufruf für Dauercheck
        self.continous_check()
            
    def sendmail(self, exam, note):
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
        try:
            send_whatsapp(f"Für {exam} hast du die Note {note_str} bekommen!")
        except:
            pass
        
        
if __name__ == '__main__':
    grades()

