from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import subprocess
import time
def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])

try:
    from bs4 import BeautifulSoup
except:
    install_bs4()
    from bs4 import BeautifulSoup

def login(username, password):
    url = "http://127.0.0.1:8000/login"
    driver.get(url)
    time.sleep(2)
    username_input = driver.find_element("name", "username")
    username_input.send_keys(username)
    password_input = driver.find_element("name", "password")
    password_input.send_keys(password)
    button = driver.find_element("xpath", "//button[text()='Log In']")
    button.click()
    time.sleep(2)

def login_success(username, password):
    try:
        url = "http://127.0.0.1:8000/login"
        driver.get(url)
        time.sleep(2)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        password_input = driver.find_element("name", "password")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Log In']")
        button.click()
        time.sleep(2)
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
        url = "http://127.0.0.1:8000/login"
        driver.get(url)
        time.sleep(2)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        password_input = driver.find_element("name", "password")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Log In']")
        button.click()
        time.sleep(2)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"

browser_options = ChromeOptions()
browser_options.headless = True
browser_options.add_argument('--ignore-certificate-errors-spki-list')
browser_options.add_argument('--ignore-ssl-errors')
browser_options.add_argument('log-level=3')
driver = Chrome(options=browser_options)

# ADD TEST CASES HERE
# At the start of each function, call the login function at the top of the page
print(f"{'Login success':<25} {login_success("sam", "testpassword")}")
print(f"{'Login failed':<25} {login_failed("sam", "test")}")

driver.quit()