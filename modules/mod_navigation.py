from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from ..main import Main


class qis_navigation():
    def __init__(self):
        ### XPaths
        self.noten_xpath = '//*[@id="navi-main"]/li[3]/a'


        ### Mapping 
        self.semester_map = {
            1: "1. Semester",
            2: "2. Semester",
            3: "3. Semester",
            4: "4. Semester",
            5: "5. Semester",
            6: "6. Semester",
            7: "7. Semester"
        }

    def run(self, driver, selected_semester):
        """
            driver: driver-object
            selected_semester: Int (1 - 7)

        """
        Main._set_state("qis_navigation: Navigiere in das Semester %d" % selected_semester)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, self.noten_xpath))).click()
        smester_partial_text = self.semester_map.get(selected_semester)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, smester_partial_text))).click()
        


if __name__ == '__main__':
    qis_navigation.run()
