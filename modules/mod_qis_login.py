from _localconfig import config

class qis_login():
    def __init__(self):
        ### XPaths
        self.username_xpath = '//*[@id="username"]'
        self.password_xpath = '/*[@id="password"]'
        self.login_button_xpath = '//*[@id="content"]/div/div/div[2]/form/div/div[2]/input'

    def run(self, driver, qis_uname, qis_pword):
        """
            driver: driver-object
            qis_uname: String
            qis_pword: String
        
        """
        driver.find_element_by_xpath(self.username_xpath).send_keys(qis_uname)
        driver.find_element_by_xpath(self.username_xpath).send_keys(qis_pword)
        driver.find_element_by_xpath(self.login_button_xpath).click()
        

            

if __name__ == '__main__':
    qis_login.run()
