import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.select import Select
import sys
import os
import time

class EndToEnd(unittest.TestCase):
    def test_endToEnd(self):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.chromeDriverManager = ChromeDriverManager()
        self.driver = webdriver.Chrome(self.chromeDriverManager.install())
        self.login()
        self.dashboardOne()
        self.newRunOne()
        self.newRunTwo()
        self.newRunThree()
        self.newRunFour()
        self.newRunFive()
        self.manageRun()
        self.driver.quit()

    def login(self):
        self.driver.maximize_window()
        self.driver.get("http://127.0.0.1:5001/")
        elem = self.driver.find_element_by_id("username")
        elem.send_keys("Admin")
        elem = self.driver.find_element_by_id("password")
        elem.send_keys("admin")
        elem.send_keys(Keys.RETURN)

    def dashboardOne(self):
        self.checkForElement("new_run_link", 2)
        elem = self.driver.find_element_by_id("new_run_link")
        elem.click()

    def newRunOne(self):
        self.checkForElement("text-input", 2)
        elem = self.driver.find_element_by_id("text-input")
        elem.send_keys("Selenium Test 1")
        elem = self.driver.find_element_by_id("textarea-answer")
        elem.send_keys("A test run in selenium ")
        elem.send_keys(Keys.RETURN)

    def newRunTwo(self):
        self.checkForElement("s_month", 2)
        elem = Select(self.driver.find_element_by_id('s_month'))
        elem.select_by_value("12")
        elem = Select(self.driver.find_element_by_id('s_year'))
        elem.select_by_value("2017")
        elem = self.driver.find_element_by_id("save_and_continue")
        elem.click()

    def newRunThree(self):
        self.checkForElement("save_and_continue", 5)
        elem = self.driver.find_element_by_id("save_and_continue")
        elem.click()

    def newRunFour(self):
        self.checkForElement("savec", 5)
        elem = self.driver.find_element_by_id("savec")
        elem.click()

    def newRunFive(self):
        self.checkForElement("survey_file", 5)
        print(self.dir_path)
        elem = self.driver.find_element_by_id("survey_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Survey.csv")
        elem = self.driver.find_element_by_id("shift_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Shift.csv")
        elem = self.driver.find_element_by_id("nr_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Non_Response.csv")
        elem = self.driver.find_element_by_id("us_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Unsampled.csv")
        elem = self.driver.find_element_by_id("tunnel_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Tunnel.csv")
        elem = self.driver.find_element_by_id("sea_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Sea.csv")
        elem = self.driver.find_element_by_id("air_file")
        elem.send_keys(self.dir_path+"/test_upload_files/Air.csv")
        elem = self.driver.find_element_by_id("savec")
        elem.click()

    def manageRun(self):
        self.checkForElement("run_button", 45)
        elem = self.driver.find_element_by_id("run_button")
        time.sleep(2)
        elem.click()
        time.sleep(5)
        self.checkVisability("cancel_button", 20)
        elem = self.driver.find_element_by_id("cancel_button")
        elem.click()
        time.sleep(10)

    def checkForElement(self, el_id, delay):
        try:
            elem = WebDriverWait(self.driver, delay).until(EC.presence_of_element_located((By.ID, el_id)))
        except TimeoutException:
            print("Loading for "+el_id+" took too much time!")
            sys.exit()

    def checkVisability(self, el_id, delay):
        try:
            element = WebDriverWait(self.driver, delay).until(
                EC.visibility_of_element_located((By.ID, el_id))
            )
        except TimeoutException:
            print("Loading for " + el_id + " took too much time!")
            sys.exit()
