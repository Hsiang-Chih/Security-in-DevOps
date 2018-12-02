# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from ddt import ddt, data, unpack
import csv
import unittest, time, re
# from csv_loader import get_csv_data

@ddt
class TestFireSignIn(unittest.TestCase):
    def get_csv_data(csv_path):
        rows = []
        csv_data = open(str(csv_path), "rb")
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)
        return rows
	
    @classmethod
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    @data(*get_csv_data("sqli.csv"))
    @unpack
    def test_fire_sign_in(self, username, password):
        driver = self.driver
        
        driver.get("http://demo.testfire.net/bank/login.aspx")
        driver.find_element_by_id("uid").clear()
        driver.find_element_by_id("uid").send_keys(username)
        driver.find_element_by_id("passw").clear()
        driver.find_element_by_id("passw").send_keys(password)
        driver.find_element_by_name("btnSubmit").click()
    
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
		
    @classmethod
    def tearDown(self):
        self.driver.quit()
        
	

	
if __name__ == "__main__":
    unittest.main()
	
