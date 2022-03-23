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

class Forever():
    def __init__(self):
        # Schließe vorherige Sessions
        os.system('pkill -f forever')


        # Initialisiere Firebase 
        
        cred = credentials.Certificate('/home/pi/bin/check-my-grades/bot_creds.json')
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()


        tz = pytz.timezone('Europe/Berlin')
        now = datetime.datetime.now(tz)
        datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
        data = {"started" : datestring}
        self.doc_ref = self.db.collection(u'bots').document(u'check_grades')
        self.doc_ref.update(data)

        # Leere History
        self._set_restarts(0)
        history_data = {"history":[]}
        self.doc_ref.update(history_data)

        self.counter = -1
        clear = lambda: os.system('clear')

        while True:
            tz = pytz.timezone('Europe/Berlin')
            now = datetime.datetime.now(tz)
            datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
            
            # Starte Check_grades
            self.counter += 1
            if self.counter != 0:
                self._set_restarts(self.counter)
                self._set_history(now.strftime("%H:%M:%S"))
            p = Popen("python /home/pi/bin/check-my-grades/check_grades.py", shell=True)
            
            ### Fehler ###
            self._set_error(now.strftime("%H:%M:%S"))
            clear()
            p.wait()
            sleep(10)
            
    def _set_history(self, datum):
        self.doc_ref.update({u'history': firestore.ArrayUnion([datum])})

    def _set_restarts(self, i):
        data = {"automated_restarts": str(i)}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)

    def _set_error(self, time):
        self.doc_ref.update({u'errors': firestore.ArrayUnion([time])})

if __name__ == '__main__':
    Forever()
