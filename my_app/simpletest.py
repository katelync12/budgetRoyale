from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import subprocess
import time
import sys
import uuid

#define global variables
buffer_constant = .1
failed = False
browser_options = ChromeOptions()
browser_options.add_argument("--headless")
#browser_options.headless = False
browser_options.add_argument("window-size=1400,1500")
browser_options.add_argument("--disable-gpu")
browser_options.add_argument("--no-sandbox")
browser_options.add_argument("start-maximized")
browser_options.add_argument("enable-automation")
browser_options.add_argument("--disable-infobars")
browser_options.add_argument("--disable-dev-shm-usage")
browser_options.add_argument('--ignore-certificate-errors-spki-list')
browser_options.add_argument('--ignore-ssl-errors')
browser_options.add_argument("--disable-web-security")
browser_options.add_argument('log-level=3')
driver = Chrome(options=browser_options)
url_head = "http://127.0.0.1:8000"

def run():
    try:
        from bs4 import BeautifulSoup
    except:
        install_bs4()
        from bs4 import BeautifulSoup
    

# ADD TEST CASES HERE
# At the start of each function, call the login function at the top of the page
    failed = False
    username = str(uuid.uuid4())[:20]
    password="testpassword"
    temp_result = login_failed("sam", "test")
    print(f"{'Login failed':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = login_success("sameeeeeee", "testpassword")
    print(f"{'Login success':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    login_logout("sam", "testpassword")

def login_success(username, password):
    try:
        url = url_head + "/login/"
        driver.get(url)
        time.sleep(buffer_constant)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        password_input = driver.find_element("name", "password")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Log In']")
        button.click()
        time.sleep(buffer_constant)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Failed")
        except TimeoutException:
            return ("Passed")
    except:
        return "Failed"

def login_failed(username, password):
    try:
        url = url_head + "/login/"
        driver.get(url)
        time.sleep(buffer_constant)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        password_input = driver.find_element("name", "password")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Log In']")
        button.click()
        time.sleep(buffer_constant)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"

def login_logout(username, password):
    try:
        url = url_head
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Profile")]')
        button.click()
        button = driver.find_element("xpath", '//button[contains(text(), "Log Out")]')
        button.click()
    except:
        return "Failed"
    
#main declaration
if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Usage: python test.py [url]")
        sys.exit(1)
    elif len(sys.argv) == 2:
        url_head = sys.argv[1]
    try:
        run()
    except AssertionError as e:
        print(e)
        exit(1)