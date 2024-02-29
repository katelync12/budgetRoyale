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
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        # Clicking on the desired option ("Transportation")
        dropdown = driver.find_element(By.ID, "type")
        dropdown.click()
        option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
        option_transportation.click()
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
    
def edit_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing Transaction']")
        row_element = row.find_element("xpath", "./parent::tr")
        edit = row_element.find_element("xpath", ".//i[@class='fas fa-pencil-alt fa-fw my-own-icon']")
        edit.click()
        time.sleep(1)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.clear()
        transaction_name.send_keys("Testing Edited")
        submit = driver.find_element("xpath", '//button[contains(text(), "Save")]')
        submit.click()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
        return "Passed"
    except:
        "Failed"
    
def cancel_delete_transaction():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing Edited']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.dismiss()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
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
        row = driver.find_element("xpath", "//th[text()='Testing Edited']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
        
def create_personal_goal():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Goal")]')
        return "Passed"
    except:
        return "Failed"
    
def create_personal_goal():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Goal")]')
        return "Passed"
    except:
        return "Failed"
    
def create_personal_goal_negative_amount():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("-100.30")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        assert "/personal-goals/create" in driver.current_url, "URL path is not '/personal_goals'"
        return "Passed"
    except:
        return "Failed"
    
def create_personal_goal_dates_error():
    try:
        login("sam", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2005")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2004")
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"
def savings_personal_goal_value_groceries():
    try:
        #create transaction
        login("test-sum-transaction", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("10")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        #nav to personal goals
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        return "Passed"
    except:
        return "Failed"
    
def savings_personal_goal_value_transportation():
    try:
        #create transaction
        login("test-sum-transaction", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("10")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2004")
        dropdown = driver.find_element(By.ID, "type")
        dropdown.click()
        option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
        option_transportation.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        #nav to personal goals
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        return "Passed"
    except:
        return "Failed"
    
def spendings_personal_goal_value_groceries():
    try:
        #create transaction
        login("test-sum-transaction", "testpassword")
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(2)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("10")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2004")
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(2)
        #nav to personal goals
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(2)
        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(2)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        #should be 0
        return "Passed"
    except:
        return "Failed"

browser_options = ChromeOptions()
browser_options.headless = False
browser_options.add_argument('--ignore-certificate-errors-spki-list')
browser_options.add_argument('--ignore-ssl-errors')
browser_options.add_argument("--disable-web-security")
browser_options.add_argument('log-level=3')
driver = Chrome(options=browser_options)

# ADD TEST CASES HERE
# At the start of each function, call the login function at the top of the page
'''temp_result = login_failed("sam", "test")
print(f"{'Login failed':<30} {temp_result}")
temp_result = login_success("sam", "testpassword")
print(f"{'Login success':<30} {temp_result}")
temp_result =login_failed("sam", "test")
print(f"{'Login failed':<30} {temp_result}")'''
temp_result = create_transaction()
print(f"{'Create transaction':<30} {temp_result}")
'''temp_result = cancel_transaction()
print(f"{'Cancel transaction':<30} {temp_result}")
temp_result = edit_transaction()
print(f"{'Edit transaction':<30} {temp_result}")
temp_result = cancel_delete_transaction()
print(f"{'Cancel delete transaction':<30} {temp_result}")
temp_result = delete_transaction()
print(f"{'Delete transaction':<30} {temp_result}")
temp_result = create_personal_goal()
print(f"{'Create personal goal':<30} {temp_result}")'''
#temp_result = create_personal_goal_negative_amount()
#print(f"{'Attempt to create goal with negative amount':<30} {temp_result}")
#temp_result = create_personal_goal_dates_error()
#print(f"{'Attempt to create goal with invalid date':<30} {temp_result}")

driver.quit()