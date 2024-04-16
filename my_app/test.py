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
browser_options.headless = False
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
    temp_result = login_success("sam", "testpassword")
    print(f"{'Login success':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    login_logout("sam", "testpassword")
    temp_result = create_account_error(username, password)
    print(f"{'Create account error':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_account(username, password)
    print(f"{'Create account':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = spendings_total_zero(username, password)
    print(f"{'Spendings total no transactions':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = date_toggle_spendings_total(username, password)
    print(f"{'Date Toggle Spendings Total':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = nav_bar_view_transaction(username, password)
    print(f"{'Nav Bar View Transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = nav_bar_personal_goal(username, password)
    print(f"{'Nav Bar Personal Goal':<45} {temp_result}")
    if temp_result == "Failed":
        print("intitialized")
        failed = True
    temp_result = streak(username, password)
    print(f"{'New account streak':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = same_day_login_streak(username, password)
    print(f"{'Same Day Login Streak':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_transaction(username, password)
    print(f"{'Create transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = cancel_transaction(username, password)
    print(f"{'Cancel transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = edit_transaction(username, password)
    print(f"{'Edit transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = cancel_delete_transaction(username, password)
    print(f"{'Cancel delete transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_transaction(username, password)
    print(f"{'Delete transaction':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_personal_goal(username, password)
    print(f"{'Create personal goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = edit_personal_goal(username, password)
    print(f"{'Edit personal goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_personal_goal(username, password)
    print(f"{'Delete personal goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_personal_goal_negative_amount(username, password)
    print(f"{'Goal w/ Neg Amount':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_personal_goal_dates_error(username, password)
    print(f"{'Goal w/ Invalid Date':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    create_personal_goal_custom(username, password)
    temp_result = create_six_goals(username, password)
    print(f"{'Create six goals':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = savings_personal_goal_value_groceries(username, password)
    print(f"{'Savings personal goal: Groceries':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = savings_personal_goal_value_transportation(username, password)
    print(f"{'Savings personal goal: Transportation':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = spendings_personal_goal_value_groceries(username, password)
    print(f"{'Spendings personal goal: Groceries':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = spendings_multiple_and_edit(username, password)
    print(f"{'Spendings multiple and edit':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = search_group_leaderboard(username, password)
    print(f"{'Select for the group leaderboard':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = search_group_w(username, password)
    print(f"{'Select for the group w':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_no_name(username, password)
    print(f"{'Create group with no name':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_existing_username(username, password)
    print(f"{'Create group with existing group name':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_mismatching_passwords(username, password)
    print(f"{'Create group with mismatching passwords':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_account_fail(username, password)
    print(f"{'Delete account failed':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group(username, password)
    print(f"{'Create Group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = cancel_delete_group(username, password)
    print(f"{'Cancel Delete Group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_goal(username, password)
    print(f"{'Create Group Goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = leaderboard_savings_overall_calculation(username, password)
    print(f"{'Savings Leaderboard Calculation':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = remove_member_cancel("group_test", "testpassword")
    print(f"{'Cancel remove member':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = remove_member_success("group_test", "testpassword")
    print(f"{'Success remove member':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True

    temp_result = join_link_in_group("group_test", "testpassword")
    print(f"{'User cannot join when in a group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
        
    temp_result = join_link_success("testCaseRemoveMember", "testpassword")
    print(f"{'User join group from link':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True



    temp_result = opt_out_comp("group_test", "testpassword")
    print(f"{'Opt out of competition':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = opt_in_comp("group_test", "testpassword")
    print(f"{'Opt back into competition':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_group(username, password)
    print(f"{'Delete Group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    #steps for this integration test since delete group goal doesnt exist
    temp_result = create_group(username, password)
    print(f"{'Create/join group after delete group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_goal2(username, password)
    print(f"{'Create Spendings, Nonoverall Group Goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = leaderboard_spending_calculation(username, password)
    print(f"{'Spending Leaderboard Calculation':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_group(username, password)
    #end of integration test
    temp_result = start_after_end_date("test-dates", "testpassword")
    print(f"{'Start after End Date Error':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = start_after_current_date("test-dates", "testpassword")
    print(f"{'Start after Current Date Error':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = sort_by_date("test-dates", "testpassword")
    print(f"{'Sort Transactions by Date':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = select_transportation_category("test-piechart", "testpassword")
    print(f"{'Select transportation category':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = select_groceries_category("test-piechart", "testpassword")
    print(f"{'Select only groceries category':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = admin_leave_group("group_test", "testpassword")
    print(f"{'No leave group option for admin':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = join_group(username, password)
    print(f"{'Member joining group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = member_leave_group(username, password)
    print(f"{'Member leaving group':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = transaction_not_in_past_week(username, password)
    print(f"{'Transaction not within past week':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = savings_total_large(username, password)
    print(f"{'Savings Total Large Number':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_account_success(username, password)
    print(f"{'Delete account':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = create_group_goal_edit("user1", "testpassword")
    print(f"{'Create group goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = edit_group_goal("user1", "testpassword")
    print(f"{'Edit group goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = delete_group_goal("user1", "testpassword")
    print(f"{'Delete group goal':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = spendings_breakdown_transaction("new12", "qwerty098")
    print(f"{'Transaction with breakdown':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True
    temp_result = spendings_breakdown_transaction_not_range("new12", "qwerty098")
    print(f"{'Transaction with breakdown - not in range':<45} {temp_result}")
    if temp_result == "Failed":
        failed = True


    driver.quit()
    assert not failed, "Not all test cases passed"

def install_bs4():
    subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
def login(username, password):
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
    
def create_transaction(username, password):
    try:
        time.sleep(buffer_constant)
        login(username, password)
        url = url_head + "/transactions/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
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
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Transaction")]')
        return "Passed"
    except:
        return "Failed"
    
def create_transaction_large(username, password):
    try:
        time.sleep(buffer_constant)
        login(username, password)
        url = url_head + "/transactions/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing Transaction")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("1200")
        date = driver.find_element(By.ID, "date")
        date.send_keys("03/30/2024")
        dropdown = driver.find_element(By.ID, "type")
        dropdown.click()
        option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
        option_transportation.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Transaction")]')
        return "Passed"
    except:
        return "Failed"
    
def create_account(username, password):
    try:
        url = url_head + "/accounts/signup/"
        driver.get(url)
        time.sleep(buffer_constant)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        email_input = driver.find_element("name", "email")
        email_input.send_keys("teambudgetroyale@gmail.com")
        password_input = driver.find_element("name", "password1")
        password_input.send_keys(password)
        password_input = driver.find_element("name", "password2")
        password_input.send_keys(password)
        button = driver.find_element("xpath", "//button[text()='Sign Up']")
        button.click()
        time.sleep(2)
        return "Passed"
    except:
        return "Failed"
    
def create_account_error(username, password):
    try:
        url = url_head + "/accounts/signup/"
        driver.get(url)
        time.sleep(buffer_constant)
        username_input = driver.find_element("name", "username")
        username_input.send_keys(username)
        email_input = driver.find_element("name", "email")
        email_input.send_keys("teambudgetroyale@gmail.com")
        password_input = driver.find_element("name", "password1")
        password_input.send_keys(password)
        password_input = driver.find_element("name", "password2")
        password_input.send_keys(password + "jfdalk")
        button = driver.find_element("xpath", "//button[text()='Sign Up']")
        button.click()
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"

def cancel_transaction(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing Cancelled")
        submit = driver.find_element("xpath", '//button[contains(text(), "Back")]')
        submit.click()
        time.sleep(buffer_constant)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Cancelled")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def edit_transaction(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
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
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
        return "Passed"
    except:
        return "Failed"
    
def cancel_delete_transaction(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing Edited']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.dismiss()
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
        return "Passed"
    except:
        return "Failed"
    
def delete_transaction(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing Edited']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def create_personal_goal(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//button[@onclick=\"window.location.href='/personal-goals/create/'\"]")
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        check = driver.find_element("xpath", '//th[contains(text(), "Testing Goal")]')
        return "Passed"
    except:
        return "Failed"
def create_personal_goal_helper(name, amount_value, start_date_value, end_date_value, category_value, is_spending):
    if (True):
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys(name)
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys(amount_value)
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys(end_date_value)
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys(start_date_value)
        if (category_value):
            button = driver.find_element("xpath", "//select[@id='type']")
            button.click()
            button = driver.find_element("xpath", f"//option[@value='{category_value}']")
            button.click()
        if (is_spending):
            radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
            radio_button_spending.click()
        time.sleep(buffer_constant)

    submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
    submit.click()
    time.sleep(buffer_constant)
def create_six_goals(username, password):
    try:
        login(username, password)
        create_personal_goal_helper("1", "100.00", "06/12/2004", "06/12/2005", "", False)
        create_personal_goal_helper("2", "100.00", "06/12/2004", "06/12/2005", "Groceries", False)
        create_personal_goal_helper("3", "100.00", "06/12/2006", "06/12/2007", "", False)
        create_personal_goal_helper("4", "100.00", "06/12/2004", "06/12/2005", "", True)
        create_personal_goal_helper("5", "100.00", "06/12/2004", "06/12/2005", "Groceries", True)
        create_personal_goal_helper("6", "100.00", "06/12/2006", "06/12/2007", "", True)
        return "Passed"
    except Exception as  e:
        print(e)
        return "Failed"
def create_personal_goal_custom(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("3")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("02/28/2024")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("02/27/2024")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("6")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("02/28/2024")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("02/27/2024")
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("2")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        button = driver.find_element("xpath", "//select[@id='type']")
        button.click()
        button = driver.find_element("xpath", "//option[@value='Groceries']")
        button.click()
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("1")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("5")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        button = driver.find_element("xpath", "//select[@id='type']")
        button.click()
        button = driver.find_element("xpath", "//option[@value='Groceries']")
        button.click()
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        button = driver.find_element("xpath", '//a[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("4")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.00")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        return "Passed"
    except:
        return "Failed"
    
def edit_personal_goal(username, password):
    try:
        login(username, password)
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing Goal']")
        row_element = row.find_element("xpath", "./parent::tr")
        edit = row_element.find_element("xpath", ".//i[@class='fas fa-pencil-alt fa-fw my-own-icon']")
        edit.click()
        time.sleep(1)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.clear()
        transaction_name.send_keys("Testing Edited")
        submit = driver.find_element("xpath", '//button[contains(text(), "Save")]')
        submit.click()
        time.sleep(buffer_constant)
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
        return "Passed"
    except:
        return "Failed"

def delete_personal_goal(username, password):
    try:
        login(username, password)
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing Edited']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-personal-goal']")
        trash.click()
        time.sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def create_personal_goal_negative_amount(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//button[@onclick=\"window.location.href='/personal-goals/create/'\"]")
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("-100.30")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
        assert "/personal-goals/create" in driver.current_url, "URL path is not '/personal_goals'"
        return "Passed"
    except:
        return "Failed"
    
def create_personal_goal_dates_error(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//button[@onclick=\"window.location.href='/personal-goals/create/'\"]")
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2004")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2005")
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"
def savings_personal_goal_value_groceries(username, password):
    try:
        #create transaction
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("10")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2004")
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        time.sleep(5)

        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        # should be 10
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(buffer_constant)

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        return "Passed"
    except:
        return "Failed"
    
def savings_personal_goal_value_transportation(username, password):
    try:
        #create transaction
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
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
        time.sleep(buffer_constant)
        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(buffer_constant)

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        return "Passed"
    except:
        return "Failed"
    
def spendings_personal_goal_value_groceries(username, password):
    try:
        #create transaction
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
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
        time.sleep(buffer_constant)
        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)
        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(buffer_constant)

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        return "Passed"
    except:
        return "Failed"
    
def spendings_multiple_and_edit(username, password):
    try:
        #create transaction
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
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
        #create second one of transportation
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys("Testing2")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("10")
        date = driver.find_element(By.ID, "date")
        date.send_keys("06/12/2005")
        dropdown = driver.find_element(By.ID, "type")
        dropdown.click()
        option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
        option_transportation.click()
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        #edit the 2nd one to amount of 1, and type of groceries
        row = driver.find_element("xpath", "//th[text()='Testing2']")
        row_element = row.find_element("xpath", "./parent::tr")
        edit = row_element.find_element("xpath", ".//i[@class='fas fa-pencil-alt fa-fw my-own-icon']")
        edit.click()
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.clear()
        amount.send_keys("1")
        dropdown = driver.find_element(By.ID, "type")
        dropdown.click()
        option_groceries = driver.find_element("xpath", "//option[text()='Groceries']")
        option_groceries.click()
        time.sleep(buffer_constant)
        submit = driver.find_element("xpath", '//button[contains(text(), "Save")]')
        submit.click()

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #check all values to see if they are correct
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        row = driver.find_element("xpath", "//th[text()='2']")
         #should be 0
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '11.00')]")
        #should be 11
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '11.00')]")
        #should be 11
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing2']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(buffer_constant)

        #nav to personal goals
        url = url_head + "/personal-goals-test/"
        driver.get(url)
        time.sleep(buffer_constant)

        #check values again
        row = driver.find_element("xpath", "//th[text()='1']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='2']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='3']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0
        row = driver.find_element("xpath", "//th[text()='4']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='5']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '10.00')]")
        #should be 10
        row = driver.find_element("xpath", "//th[text()='6']")
        row_element = row.find_element("xpath", "./parent::tr")
        confirm = row_element.find_element("xpath", ".//th[contains(text(), '0.00')]")
        #should be 0

        #delete transaction
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        row = driver.find_element("xpath", "//th[text()='Testing']")
        row_element = row.find_element("xpath", "./parent::tr")
        trash = row_element.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-transaction']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(buffer_constant)
        return "Passed"
    except:
        return "Failed"
def delete_account_fail(username, password):
    try:
        login(username, password)
        url = url_head + "/settings/"
        driver.get(url)
        button = driver.find_element("xpath", "//button[text()='Delete Account']")
        button.click()
        time.sleep(2)
        prompt = driver.switch_to.alert
        prompt.send_keys("HelloHello")
        prompt.accept()
        time.sleep(1)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"
    
def delete_account_success(username, password):
    try:
        login(username, password)
        url = url_head + "/settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//button[text()='Delete Account']")
        button.click()
        time.sleep(2)
        prompt = driver.switch_to.alert
        prompt.send_keys(username)
        prompt.accept()
        
        try:
            button = driver.find_element("xpath", "//button[text()='Delete Account']")
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def start_after_end_date(username, password):
    try:
        login(username, password)
        date = driver.find_element(By.ID, "start_date")
        date.send_keys("06/12/2004")
        date = driver.find_element(By.ID, "end_date")
        date.send_keys("06/10/2004")
        button = driver.find_element("xpath", "//button[@onclick='submitDates()']")
        button.click()
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"
    
def start_after_current_date(username, password):
    try:
        login(username, password)
        date = driver.find_element(By.ID, "start_date")
        date.send_keys("06/12/3000")
        button = driver.find_element("xpath", "//button[@onclick='submitDates()']")
        button.click()
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"
    
def sort_by_date(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        date = driver.find_element(By.ID, "end_date")
        date.send_keys("03/10/2024")
        button = driver.find_element("xpath", "//button[@onclick='filterTransactions()']")
        button.click()
        time.sleep(buffer_constant)
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Walmart")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def select_transportation_category(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//label[@class='dropdown-label']")
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//input[@type='checkbox' and @name='selected_categories' and @value='Transportation']")
        button.click()
        button = driver.find_element("xpath", "//button[@type='button' and @onclick='submitForm()']")
        button.click()
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Uber")]')
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Walmart")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
    
def select_groceries_category(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//label[@class='dropdown-label']")
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//input[@type='checkbox' and @name='selected_categories' and @value='Groceries']")
        button.click()
        button = driver.find_element("xpath", "//input[@type='checkbox' and @name='selected_categories' and @value='Transportation']")
        button.click()
        button = driver.find_element("xpath", "//button[@type='button' and @onclick='submitForm()']")
        button.click()
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//th[contains(text(), "Walmart")]')
        try:
            check = driver.find_element("xpath", '//th[contains(text(), "Uber")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def search_group_leaderboard(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/"
        driver.get(url)
        time.sleep(buffer_constant)
        search_input = driver.find_element(By.ID, "search_input")
        search_input.click()
        search_input.send_keys("leaderboard")
        search_button = driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//p[@class='group_name_label' and contains(text(), 'leaderboard')]")
        try:
            button = driver.find_element("xpath", "//p[@class='group_name_label' and contains(text(), 'testGroup')]")
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def search_group_w(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/"
        driver.get(url)
        time.sleep(buffer_constant)
        search_input = driver.find_element(By.ID, "search_input")
        search_input.click()
        search_input.send_keys("w")
        search_button = driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//p[@class='group_name_label' and contains(text(), 'w')]")
        try:
            button = driver.find_element("xpath", "//p[@class='group_name_label' and contains(text(), 'testGroup')]")
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def create_group_no_name(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/create/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//button[contains(@style, 'background-color: #5B5FC5;') and contains(@style, 'color: #ffffff;') and contains(@style, 'cursor: pointer;')]")
        button.click()
        time.sleep(buffer_constant)
        try:
            label_element = driver.find_element(By.XPATH, "//label[@for='name' and text()='Name your group!'][@style='font-size: medium; font-family: Verdana, Geneva, Tahoma, sans-serif;']")
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"
    
def create_group_existing_username(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/create/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//input[@style='width: 80%;'][@type='text'][@id='name']")
        button.send_keys("w")
        button = driver.find_element("xpath", "//button[contains(@style, 'background-color: #5B5FC5;') and contains(@style, 'color: #ffffff;') and contains(@style, 'cursor: pointer;')]")
        button.click()
        time.sleep(buffer_constant)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            time.sleep(buffer_constant)
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"
    
def create_group_mismatching_passwords(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/create"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", "//input[@style='width: 80%;'][@type='text'][@id='name']")
        button.send_keys("testing4325")
        password_input = driver.find_element(By.NAME, "password1")
        password_input.send_keys("test")
        password_input = driver.find_element(By.NAME, "password2")
        password_input.send_keys("testing")
        button = driver.find_element("xpath", "//button[contains(@style, 'background-color: #5B5FC5;') and contains(@style, 'color: #ffffff;') and contains(@style, 'cursor: pointer;')]")
        button.click()
        time.sleep(buffer_constant)
        try:
            alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
            alert.accept()
            time.sleep(buffer_constant)
            return ("Passed")
        except TimeoutException:
            return ("Failed")
    except:
        return "Failed"

def create_group(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Leaderboard")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create Group")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Name']")
        transaction_name.send_keys("AUTOMATED_TEST_GROUP")
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create Group")]')
        button.click()
        time.sleep(1)
        group_element = driver.find_element("xpath", "//*[contains(text(), 'AUTOMATED_TEST_GROUP')]")
        return "Passed"
    except Exception as e:
        #print(e)
        return "Failed"
    
def cancel_delete_group(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group Settings")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Delete Group")]')
        button.click()
        time.sleep(buffer_constant)
        alert = driver.switch_to.alert
        alert.dismiss()
        time.sleep(1)
        check = driver.find_element("xpath", '//button[contains(text(), "Delete Group")]')
        return "Passed"
    except:
        return "Failed"
    
def delete_group(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group Settings")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Delete Group")]')
        button.click()
        time.sleep(buffer_constant)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(2)
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert.accept()
        #check = driver.find_element("xpath", '//button[contains(text(), "Create Group")]')
        return "Passed"
    except Exception as e:
        #print(e)
        return "Failed"

def create_transaction_subroutine(name, amount, date, is_spending, category):
        url = url_head + "/transactions/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys(name)
        amount_t = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount_t.send_keys(amount)
        date1 = driver.find_element(By.ID, "date")
        date1.send_keys(date)
        if (is_spending):
            radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
            radio_button_spending.click()
        # Clicking on the desired option ("Transportation")
        if(category):
            dropdown = driver.find_element(By.ID, "type")
            dropdown.click()
            #option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
            option_category = driver.find_element("xpath", f"//option[text()='{category}']")
            option_category.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

def create_transaction_with_group_goal_subroutine(name, amount, date, is_spending, category, group_goal):
        url = url_head + "/transactions/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Transaction Name']")
        transaction_name.send_keys(name)
        amount_t = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount_t.send_keys(amount)
        date1 = driver.find_element(By.ID, "date")
        date1.send_keys(date)
        if (is_spending):
            radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
            radio_button_spending.click()
        # Clicking on the desired option ("Transportation")
        if(category):
            dropdown = driver.find_element(By.ID, "type")
            dropdown.click()
            #option_transportation = driver.find_element("xpath", "//option[text()='Transportation']")
            option_category = driver.find_element("xpath", f"//option[text()='{category}']")
            option_category.click()
        if(group_goal):
            dropdown = driver.find_element(By.NAME, "group_goal")
            dropdown.click()
            option_category = driver.find_element("xpath", f"//option[text()='{group_goal}']")
            option_category.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)

def create_group_goal(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Group Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Group Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        checkbox = driver.find_element("xpath", "//input[@type='checkbox' and @name='is_primary']")
        if not checkbox.is_selected():
            # If not selected, click the checkbox to select it
            checkbox.click()
        checkbox = driver.find_element("xpath", "//input[@type='checkbox' and @name='is_overall']")
        if not checkbox.is_selected():
            # If not selected, click the checkbox to select it
            checkbox.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
    #   TODO: CONFIRM WE HAVE LANDED ON THE RIGHT PAGE
        return "Passed"
    except Exception as e:
        #print(e)
        return "Failed"
    
def create_group_goal2(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Group Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Group Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        radio_button_spending = driver.find_element("xpath", "//input[@type='radio' and @value='on']")
        radio_button_spending.click()
        checkbox = driver.find_element("xpath", "//input[@type='checkbox' and @name='is_primary']")
        if not checkbox.is_selected():
            # If not selected, click the checkbox to select it
            checkbox.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
    #   TODO: CONFIRM WE HAVE LANDED ON THE RIGHT PAGE
        return "Passed"
    except:
        return "Failed"
    
def leaderboard_savings_overall_calculation(username, password):
    try:
        login(username, password)
        create_transaction_subroutine("No category savings", "10" ,"06/12/2004", False, "")
        create_transaction_subroutine("Category savings", "5" ,"06/12/2004", False, "Transportation")
        create_transaction_subroutine("Out of range savings", "2" ,"06/12/2003", False, "Transportation")
        create_transaction_subroutine("No category spending", "1" ,"06/12/2004", True, "")
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Leaderboard")]')
        button.click()
        time.sleep(2)
        user_entry = driver.find_element("xpath", f"//div[@class='leaderboard-entry']//div[@class='left-content']//span[@class='player-name' and contains(text(), '{username}')]")
        right_content = user_entry.find_element("xpath", ".//ancestor::div[@class='leaderboard-entry']//div[@class='right-content']")
        # Find the span with class player-score and get its text (assuming it contains the score)
        score_span = right_content.find_element("xpath", ".//span[@class='player-score']")
        score = float(score_span.text)
        if (score == 15.0):
            return "Passed"
        return "Failed"
    except Exception as e:
        print(e)
        return "Failed"
    
def admin_leave_group(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        try:
            check = driver.find_element("xpath", '//button[contains(text(), "Leave Group")]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"

def join_group(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/"
        driver.get(url)
        time.sleep(buffer_constant)
        # group_to_join = driver.find_element("xpath", '//p[@class="group_name_label" and text()="w"]/following-sibling::div/button[text()="Join Group"]')
        group_to_join = driver.find_element("xpath", '//p[@class="group_name_label" and text()="w"]/following-sibling::div[contains(@class, "button-container")]/button[text()="Join Group"]')
        group_to_join.click()
        time.sleep(buffer_constant)  
        password_input = driver.find_element("xpath", '//input[@type="password" and @name="password"]')
        password_input.send_keys("123")
        button = driver.find_element("xpath", '//button[contains(text(), "Join!")]')
        button.click()
        button = driver.find_element("xpath", '//h2[@class="group-members-settings"]')
        time.sleep(buffer_constant)
        return "Passed"
    except:
        return "Failed"

def member_leave_group(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        check = driver.find_element("xpath", '//button[contains(text(), "Leave Group")]')
        check.click()

        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        join = driver.find_element("xpath", './/input[@id="search_input"]')
        return "Passed"
    except:
        return "Failed"

def leaderboard_spending_calculation(username, password):
    try:
        login(username, password)
        create_transaction_with_group_goal_subroutine("No category savings", "10" ,"06/12/2004", True, "", "Testing Group Goal")
        create_transaction_with_group_goal_subroutine("No category savings", "10" ,"06/12/2004", True, "", "")
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Leaderboard")]')
        button.click()
        time.sleep(2)
        user_entry = driver.find_element("xpath", f"//div[@class='leaderboard-entry']//div[@class='left-content']//span[@class='player-name' and contains(text(), '{username}')]")
        right_content = user_entry.find_element("xpath", ".//ancestor::div[@class='leaderboard-entry']//div[@class='right-content']")
        # Find the span with class player-score and get its text (assuming it contains the score)
        score_span = right_content.find_element("xpath", ".//span[@class='player-score']")
        score = float(score_span.text)
        if (score == -10.0):
            return "Passed"
        return "Failed"
    except:
        return "Failed"
    
def spendings_total_zero(username, password):
    try:
        login(username, password)
        expenses_total_element = driver.find_element(By.ID, "expenses_total")
        expenses_total_text = expenses_total_element.text
        if expenses_total_text == "$0.00":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"
    
def transaction_not_in_past_week(username, password):
    try:
        create_transaction(username, password)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Dashboard")]')
        button.click()
        time.sleep(buffer_constant)
        expenses_total_element = driver.find_element(By.ID, "expenses_total")
        expenses_total_text = expenses_total_element.text
        if expenses_total_text == "$0.00":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"
    
def date_toggle_spendings_total(username, password):
    try:
        login(username, password)
        date = driver.find_element(By.ID, "start_date")
        date.send_keys("06/10/2004")
        button = driver.find_element("xpath", "//button[@onclick='submitDates()']")
        button.click()
        time.sleep(1)
        expenses_total_element = driver.find_element(By.ID, "expenses_total")
        expenses_total_text = expenses_total_element.text
        if expenses_total_text == "$0.00":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"
    
def savings_total_large(username, password):
    try:
        create_transaction_large(username, password)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Dashboard")]')
        button.click()
        time.sleep(buffer_constant)
        date = driver.find_element(By.ID, "start_date")
        date.send_keys("03/29/2024")
        button = driver.find_element("xpath", "//button[@onclick='submitDates()']")
        button.click()
        time.sleep(1)
        expenses_total_element = driver.find_element(By.ID, "income_total")
        expenses_total_text = expenses_total_element.text
        if expenses_total_text == "$1.20K":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"
    
def streak(username, password):
    try:
        login(username, password)
        streak = driver.find_element(By.ID, "streak")
        streak_text = streak.text
        if streak_text == "1":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"
    
def same_day_login_streak(username, password):
    try:
        login(username, password)
        streak = driver.find_element(By.ID, "streak")
        streak_text = streak.text
        if streak_text == "1":
            return "Passed"
        else:
            return "Failed"
    except:
        return "Failed"

def create_group_goal_edit(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Group Goals")]')
        button.click()
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[contains(text(), "Create")]')
        button.click()
        time.sleep(buffer_constant)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.send_keys("Testing Group Goal")
        amount = driver.find_element("xpath", "//input[@placeholder='Amount']")
        amount.send_keys("100.30")
        end_date = driver.find_element(By.ID, "end_date")
        end_date.send_keys("06/12/2005")
        start_date = driver.find_element(By.ID, "start_date")
        start_date.send_keys("06/12/2004")
        checkbox = driver.find_element("xpath", "//input[@type='checkbox' and @name='is_overall']")
        if not checkbox.is_selected():
            # If not selected, click the checkbox to select it
            checkbox.click()
        submit = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit.click()
        time.sleep(buffer_constant)
    #   TODO: CONFIRM WE HAVE LANDED ON THE RIGHT PAGE
        return "Passed"
    except Exception as e:
        #print(e)
        return "Failed"

def edit_group_goal(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_goals/"
        driver.get(url)
        time.sleep(buffer_constant)
        #row = driver.find_element("xpath", "//[text()='Edit Goal Test']")
        #row_element = row.find_element("xpath", "./parent::tr")
        edit = driver.find_element("xpath", ".//i[@class='fas fa-pencil-alt fa-fw my-own-icon']")
        edit.click()
        time.sleep(1)
        transaction_name = driver.find_element("xpath", "//input[@placeholder='Goal Name']")
        transaction_name.clear()
        transaction_name.send_keys("Testing Edited")
        submit = driver.find_element("xpath", "//button[text()='Save']")
        submit.click()
        time.sleep(buffer_constant)
        url = "http://127.0.0.1:8000/groups/group_goals/"
        driver.get(url)
        time.sleep(buffer_constant)
        #check = driver.find_element("xpath", '//a[contains(text(), "Testing Edited")]')
        text_present = driver.execute_script('return document.body.innerText.includes("Testing Edited");')
        return "Passed"
    except:
        return "Failed"
    
def delete_group_goal(username, password):
    try:
        login(username, password)
        url = "http://127.0.0.1:8000/groups/group_goals/"
        driver.get(url)
        time.sleep(buffer_constant)
       # row = driver.find_element("xpath", "//th[text()='Testing Edited']")
       # row_element = row.find_element("xpath", "./parent::tr")
        trash = driver.find_element("xpath", ".//i[@class='fas fa-trash-alt delete-goal']")
        trash.click()
        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        try:
            #check = driver.find_element("xpath", '//th[contains(text(), "Testing Edited")]')
            text_present = driver.execute_script('return document.body.innerText.includes("Testing Edited");')
            return "Passed"
        except:
            return "Passed"
    except:
        return "Failed"
    
def nav_bar_view_transaction(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Personal")]')
        button.click()
        button = driver.find_element("xpath", '//button[contains(text(), "View Transactions")]')
        button.click()
        time.sleep(buffer_constant)
        try:
            check = driver.find_element("xpath", '//h2[contains(text(), "Transactions")]')
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"
    
def nav_bar_personal_goal(username, password):
    try:
        login(username, password)
        button = driver.find_element("xpath", '//a[contains(text(), "Profile")]')
        button.click()
        button = driver.find_element("xpath", '//button[contains(text(), "Personal Goals")]')
        button.click()
        time.sleep(buffer_constant)
        try:
            check = driver.find_element("xpath", '//h2[contains(text(), "Personal Goals")]')
            return "Passed"
        except:
            return "Failed"
    except:
        return "Failed"

def remove_member_cancel(username, password):
    try:
        if join_group("testCaseRemoveMember", "testpassword") == "Failed":
            return "Failed"
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//form[@id="remove-member-formtestCaseRemoveMember"]//button[contains(@class, "remove-member-btn")]')
        button.click()
        alert = driver.switch_to.alert
        alert.dismiss()
        time.sleep(1)
        check = driver.find_element("xpath", '//form[@id="remove-member-formtestCaseRemoveMember"]')
        return "Passed"
    except:
        return "Failed"

def remove_member_success(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//form[@id="remove-member-formtestCaseRemoveMember"]//button[contains(@class, "remove-member-btn")]')
        button.click()
        alert = driver.switch_to.alert
        alert.accept()
        time.sleep(1)
        try:
            check = driver.find_element("xpath", '//form[@id="remove-member-formtestCaseRemoveMember"]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"


def opt_out_comp(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//span[@class="slider round"]')
        button.click()
        url = url_head + "/groups/leaderboard/"
        driver.get(url)
        try:
            check = driver.find_element("xpath", '//span[@class="player-name" and text()="group_test"]')
            return "Failed"
        except:
            return "Passed"
    except:
        return "Failed"

def opt_in_comp(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//span[@class="slider round"]')
        button.click()
        url = url_head + "/groups/leaderboard/"
        driver.get(url)
        check = driver.find_element("xpath", '//span[@class="player-name" and text()="group_test"]')
        return "Passed"
    except:
        return "Failed"

def join_link_in_group(username, password):
    try:
        login(username, password)
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[@class="group-settings-button" and @id="popupBtn"]')
        button.click()

        popup_text_element = driver.find_element("xpath", '//div[@id="popupText"]')
        popup_text = popup_text_element.text
        driver.get(popup_text)
        time.sleep(buffer_constant)
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert.accept()
        return "Passed"
    except:
        return "Failed"

def join_link_success(username, password):
    try:
        login("group_test", "testpassword")
        url = url_head + "/groups/group_settings/"
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//button[@class="group-settings-button" and @id="popupBtn"]')
        button.click()
        popup_text_element = driver.find_element("xpath", '//div[@id="popupText"]')
        popup_text = popup_text_element.text

        url = url_head
        driver.get(url)
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Profile")]')
        button.click()
        button = driver.find_element("xpath", '//button[contains(text(), "Log Out")]')
        button.click()

        login(username, password)
        driver.get(popup_text)
        time.sleep(buffer_constant)
        alert = WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert.accept()
        check = driver.find_element("xpath", '//button[contains(text(), "Leave Group")]')
        check.click()

        time.sleep(1)
        alert = driver.switch_to.alert
        alert.accept()

        return "Passed"
    except:
        return "Failed"




def spendings_breakdown_transaction(username, password):
    try:
        login(username, password)
        create_transaction_with_group_goal_subroutine("Testing Edited", "10" ,"04/15/2024", True, "", "")
        #create_transaction_with_group_goal_subroutine("No category savings", "10" ,"06/12/2004", True, "", "")
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Spendings Breakdown")]')
        button.click()
        time.sleep(2)
        user_entry = driver.find_element("xpath", f"//div[@class='leaderboard-entry']//div[@class='left-content']//span[@class='player-name' and contains(text(), '{username}')]")
        right_content = user_entry.find_element("xpath", ".//ancestor::div[@class='leaderboard-entry']//div[@class='right-content']")
        # Find the span with class player-score and get its text (assuming it contains the score)
        score_span = right_content.find_element("xpath", ".//span[@class='player-score']")
        #score = float(score_span.text)
        score = driver.execute_script('return document.body.innerText.includes("$10.00");')
        delete_transaction(username, password)
        if (score == True):
            return "Passed"
        return "Failed"
    except:
        return "Failed"

def spendings_breakdown_transaction_not_range(username, password):
    try:
        login(username, password)
        create_transaction_with_group_goal_subroutine("Testing Edited", "10" ,"04/15/2003", True, "", "")
        #create_transaction_with_group_goal_subroutine("No category savings", "10" ,"06/12/2004", True, "", "")
        time.sleep(buffer_constant)
        button = driver.find_element("xpath", '//a[contains(text(), "Group")]')
        button.click()
        button = driver.find_element("xpath", '//a[contains(text(), "Spendings Breakdown")]')
        button.click()
        time.sleep(2)
        user_entry = driver.find_element("xpath", f"//div[@class='leaderboard-entry']//div[@class='left-content']//span[@class='player-name' and contains(text(), '{username}')]")
        right_content = user_entry.find_element("xpath", ".//ancestor::div[@class='leaderboard-entry']//div[@class='right-content']")
        # Find the span with class player-score and get its text (assuming it contains the score)
        score_span = right_content.find_element("xpath", ".//span[@class='player-score']")
        #score = float(score_span.text)
        score = driver.execute_script('return document.body.innerText.includes("$10.00");')
        delete_transaction(username, password)
        if (score == False):
            return "Passed"
        return "Failed"
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

