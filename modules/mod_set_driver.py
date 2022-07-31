from selenium import webdriver

class Set_driver():
    def __init__ (self, driver):
        self.driver = driver

    def setUp():
        driver = webdriver.Chrome()
        return Set_driver(driver)