from modules.mod_set_driver import Set_driver
class Qis_login():
    def __init__(self):
        self.driver = Set_driver.setUp()
        ### XPaths
        self.username_xpath = '//*[@id="username"]'
        self.password_xpath = '/*[@id="password"]'
        self.login_button_xpath = '//*[@id="content"]/div/div/div[2]/form/div/div[2]/input'

    def run(self, qis_uname, qis_pword):
        """
            driver: driver-object
            qis_uname: String
            qis_pword: String
        
        """
        print("LOGIN")
        try:
            self.driver.find_element_by_xpath(self.username_xpath).send_keys(qis_uname)
            self.driver.find_element_by_xpath(self.username_xpath).send_keys(qis_pword)
            self.driver.find_element_by_xpath(self.login_button_xpath).click()
        except Exception as ex:
            print(ex)
            return False
        return True
        

            

if __name__ == '__main__':
    Qis_login.run()
