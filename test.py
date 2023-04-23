from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from functions import handle_username_dupe, check_username_dupe, find_verified_users, scroll_page, remove_duplicates_from_list, block_the_blue, confirmations

import time

#TODO: Check for no bio, add more words to ban list

email         = input("Enter your email ")
usersname     = input("Enter your username  ")
userspassword = input("Enter your password  ")
duration      = input("How long (seconds) should I scroll? (Hint: Longer = more users blocked)   ")

service       = Service(r"C:\Program Files (x86)\chromedriver.exe")
op            = webdriver.ChromeOptions()
driver        = webdriver.Chrome(service=service, options=op)
driver.get("https://twitter.com")

WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/login'] span > span"))).click()

username = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='username']")))
username.send_keys(email)

next_click = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
next_click.click()

username_dupe_check = check_username_dupe(driver)
if(username_dupe_check):
    handle_username_dupe(driver, usersname)
        
password = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@autocomplete='current-password']")))
password.send_keys(userspassword)

login_click = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='LoginForm_Login_Button']")))
login_click.click()

# Wait for the tweets to become present
wait = WebDriverWait(driver, 1000)
tweets_present = EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="cellInnerDiv"]'))
wait.until(tweets_present)

time.sleep(5)

start_time = time.time()
verified_accounts = []
while time.time() < start_time + int(duration):
    scroll_page(driver)
    verified_accounts = verified_accounts + find_verified_users(driver)

verified_accounts = remove_duplicates_from_list(verified_accounts)

confirmations(verified_accounts)
block_the_blue(driver, verified_accounts)

print("Press enter to end script!")
input()