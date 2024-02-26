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

def test_login(username, password):
    url = "http://127.0.0.1:8000/login"
    driver.get(url)
    time.sleep(2)
    try:
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        password_input = driver.find_element("name", "password")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Log In']")
        button.click()
        time.sleep(2)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            print("Login credentials are wrong")
            alert.accept()
        except TimeoutException:
            print("Login success")
            time.sleep(2)
    except:
        print("Login error")

browser_options = ChromeOptions()
browser_options.headless = True
browser_options.add_argument('--ignore-certificate-errors-spki-list')
browser_options.add_argument('--ignore-ssl-errors')
driver = Chrome(options=browser_options)

# ADD TEST CASES HERE
# At the start of each function, call the login function at the top of the page
# Include an expected output and print ..... between each test case to differentiate

# testing login success
print("Expected output: Login success")
test_login("sam", "testpassword")
print(".....")
# testing login failed
print("Expected output: Login credentials are wrong")
test_login("sam", "test")
print(".....")

driver.quit()