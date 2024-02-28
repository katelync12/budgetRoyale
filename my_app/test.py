from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
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
    
def create_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing Transaction")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("8.99")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Transaction")]')
        return "Passed"
    except:
        return "Failed"
    
def cancel_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing Cancelled")
        submit = driver.find_element("xpath", '//button[contains(text(), "Back")]')
        submit.click()
        time.sleep(2)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Cancelled")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def cancel_delete_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing Transaction']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.dismiss()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Transaction")]')
        return "Passed"
    except:
        return "Failed"
    
def delete_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing Transaction']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Transaction")]')
            return "Failed"
        except:
            return "Passed"
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
print(f"{'Login success':<30} {login_success("sam", "testpassword")}")
print(f"{'Login failed':<30} {login_failed("sam", "test")}")
print(f"{'Create transaction':<30} {(create_transaction())}")
print(f"{'Cancel transaction':<30} {cancel_transaction()}")
print(f"{'Cancel delete transaction':<30} {cancel_delete_transaction()}")
print(f"{'Delete transaction':<30} {delete_transaction()}")

driver.quit()