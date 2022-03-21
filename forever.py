from subprocess import Popen
import datetime
import os
from time import sleep
import pytz
import firebase_admin
from firebase_admin import credentials
from google.cloud import firestore
from firebase_admin import firestore

BOT_ID = "recfDz9mQYpPU99pu"
TOMORROW = "21.03.2022"


class Forever():
    def __init__(self):
        # Initialisiere Firebase 
        
        cred = credentials.Certificate('bot_creds.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()


        tz = pytz.timezone('Europe/Berlin')
        now = datetime.datetime.now(tz)
        datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
        data = {"started" : datestring}
        self.doc_ref = self.db.collection(u'bots').document(u'check_grades')
        self.doc_ref.update(data)

        # Leere History
        automated_restarts_data = {"automated_restarts": "0"}
        history_data = {"history":[]}
        self.doc_ref.update(automated_restarts_data)
        self.doc_ref.update(history_data)

        self.counter = -1
        clear = lambda: os.system('clear')

        while True:
            tz = pytz.timezone('Europe/Berlin')
            now = datetime.datetime.now(tz)
            datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
            
            # Leere History wenn neuer Tag
            if self._check_new_day(datetime.date.today()):
                history_data = {"history":[]}
                self.doc_ref.update(history_data)

            # Starte Check_grades
            self.counter += 1
            if self.counter != 0:
                self._set_restarts(self.counter)
                self._set_history(now.strftime("%H:%M:%S"))
            p = Popen("python check_grades.py", shell=True)
            clear()
            p.wait()
            sleep(20)
            
    def _check_new_day(self, today):
        global tomorrow
        tm = datetime.date.today() + datetime.timedelta(days=1)
        tomorrow = tm
        if today == tomorrow:
                tomorrow = today
                return True
        else:
                return False

    def _set_history(self, datum):
        self.doc_ref.update({u'history': firestore.ArrayUnion([datum])})

    def _set_restarts(self, i):
        data = {"automated_restarts": str(i)}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)

if __name__ == '__main__':
    Forever()
