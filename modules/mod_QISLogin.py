from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os


class QISLogin():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def run(self):
        try:
            input_username = self.driver.find_element_by_xpath("""//*[@id="username"]""").send_keys(self.username)
            input_pw = self.driver.find_element_by_xpath("""//*[@id="password"]""").send_keys(self.password)
            weiter_btn = self.driver.find_element_by_xpath("""//*[@id="content"]/div/div/div[2]/form/div/div[2]/input""").click()
        except:
            raise Exception