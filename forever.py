from subprocess import Popen
import datetime
import os
from time import sleep

FILE_NAME = "restart.txt"


class Forever():
    def __init__(self):
        self.counter = 0
        clear = lambda: os.system('cls')
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

        while True:
            now = datetime.datetime.now()
            datestring = now.strftime("%d.%m.%Y, %H:%M:%S")
            if self.counter == 0:
                f = open(FILE_NAME, "a+")
                f.write(f"--- GESTARTET - {datestring} ---\n")
                f.close()
            else:
                f = open(FILE_NAME, "a+")
                f.write(f"Fail {self.counter} - {datestring}\n")
                f.close()
            p = Popen("python check_grades.py", shell=True)
            clear()
            p.wait()
            sleep(20)
            self.counter += 1
            

if __name__ == '__main__':
    Forever()
