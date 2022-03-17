from configparser import NoSectionError
from logging import exception
from time import time


import time

class test():
    def __init__(self) -> None:
        print("init")
    def run(self):
        while True:
            try:
                print("rin")
                time.sleep(3)
                try:
                    print("nuchmal run")
                    raise NoSectionError
                except Exception as ex:
                    raise
                
                
            except:
                return

if __name__ == '__main__':
    a = test()
    for _ in range(5):
        try:
            a.run()
        except:
            raise