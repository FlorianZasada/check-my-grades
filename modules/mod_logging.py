import os
import datetime


description = """__init__()"""

class logging():
    def __init__(self):
        self.log_path_name = "_log"
        self.log_file_name = "log.txt"


        # Check if folder exists
        if not os.path.isdir(self.log_path_name):
            os.mkdir(self.log_path_name)
        # Check if file exists
        if not os.path.isfile(os.path.join(self.log_path_name, self.log_file_name)):
            open(os.path.join(self.log_path_name, self.log_file_name), 'a').close()


    def write_log(self, type: str, message: str) -> None:
        """
        params:

        message: String
            Schreibe die Message in das Logfile

        type: String
            Typ der Message ["info", "warning", "error"]
        """

        now = datetime.datetime.now().strftime("%d.%m.%Y, %H:%M:%S")

        with open(os.path.join(self.log_path_name, self.log_file_name), 'a') as logfile:
            if type == "info":
                logfile.writelines("[INFO] - "+now+" - "+ message+"\n")
            elif type == "warning":
                logfile.writelines("[WARNING] - "+now+" - "+ message+"\n")
            elif type == "error":
                logfile.writelines("[ERROR] - "+now+" - "+ message+"\n")
            else:
                raise Exception("Es wurde kein Logging Typ angegeben")

        

if __name__ == '__main__':
    logging().write_log("info", "asdf")