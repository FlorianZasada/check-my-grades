from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class navigation():
    def __init__(self):
        ### XPaths
        self.noten_xpath = '//*[@id="navi-main"]/li[3]/a'

    def run(self, driver, selected_semester):
        """
            driver: driver-object

        
        """
        self._set_state("Navigiere in das Semeseter")
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.noten_xpath))).click()
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, selected_semester))).click()
        

            

if __name__ == '__main__':
    qis_login.run()
