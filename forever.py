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
COUNTER = -1

class Forever():
    def __init__(self):
        global COUNTER

        if os.environ.get('https_proxy'):
            del os.environ['https_proxy']
        if os.environ.get('http_proxy'):
            del os.environ['http_proxy']

        # Schließe vorherige Sessions

        try:
            os.system('pkill -f check_grades')
        except:
            pass

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
        errors_data = {"errors": []}

        self.doc_ref.update(history_data)
        self.doc_ref.update(errors_data)

        self._set_runtime()

        clear = lambda: os.system('clear')

        while True:
            tz = pytz.timezone('Europe/Berlin')
            now = datetime.datetime.now(tz)
            datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
            
            # Starte Check_grades
            COUNTER += 1
            if COUNTER != 0:
                self._set_restarts(COUNTER)
                self._set_history(now.strftime("%H:%M:%S"))
                       
            p = Popen("python /home/pi/bin/check-my-grades/check_grades.py", shell=True)

            clear()
            p.wait()

            # Fehler
            now = datetime.datetime.now(tz)
            self._set_error(now.strftime("%H:%M:%S"))
            self._set_runtime(runtime="Inaktiv")
            sleep(15)

    def _set_runtime(self, runtime="Aktiv"):
        data = {"runtime": runtime}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)
            
    def _set_history(self, datum):
        self.doc_ref.update({u'history': firestore.ArrayUnion([datum])})

    def _set_restarts(self, i):
        data = {"automated_restarts": str(i)}
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update(data)

    def _set_error(self, time):
        doc_ref = self.db.collection(u'bots').document(u'check_grades')
        doc_ref.update({"errors": firestore.ArrayUnion([{"error_time": time, "error_msg": self._get_current_state()}]), "runtime": "Inaktiv"})
        # self.doc_ref.update({u'errors': firestore.ArrayUnion([{time: self._get_current_state()}])})

    def _get_current_state(self):
        state = self.doc_ref.get({u'status'})
        state_val = state.get('status')
        return state_val

if __name__ == '__main__':
    Forever()
