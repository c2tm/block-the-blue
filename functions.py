from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time
import sys

# This is where you can specify which words the script will check for in a users bio
words = []

def handle_username_dupe(driver, usersname):
    username_dupe = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']")))
    username_dupe.send_keys(usersname)
    next_click = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
    next_click.click()

def check_username_dupe(driver):
    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']")))
    except NoSuchElementException:
        return False
    return True

def find_verified_users(driver):
    # Find all tweets
    tweets = driver.find_elements(By.XPATH, '//div[@data-testid="cellInnerDiv"]')

    # Loop through the tweets and extract verified usernames
    verified_accounts = []
    for tweet in tweets:
        try:
            # Check if the account is verified
            verified_badge = tweet.find_element(By.XPATH, './/div//div//article[@data-testid="tweet"]//div//div//div[2]//div[2]//div//div//div//div//div[@data-testid="User-Name"]//div//div//a//div//div[2]//span//*[local-name() = "svg" and @data-testid="icon-verified"]')
            username = tweet.find_element(By.XPATH, './/div//div//article[@data-testid="tweet"]//div//div//div[2]//div[2]//div//div//div//div//div[@data-testid="User-Name"]//div[2]//div//div//a//div//span')
            if username.text not in verified_accounts:
                verified_accounts.append(username.text)
        except:
            # Account is not verified or there was an error, continue to the next tweet
            continue
    return verified_accounts

def scroll_page(driver):
    # Scroll down the page for x seconds
    scroll_pause_time = .25
    last_height = driver.execute_script("return document.body.scrollHeight")
    start_time = time.time()
    while (time.time() - start_time) < scroll_pause_time:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def remove_duplicates_from_list(verified_accounts):
    new_list = list(set(verified_accounts))
    return new_list

def the_scales_of_justice(driver):
    check = 0
    text = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='UserDescription']//span"))).text
    for word in words:
        try:
            if text.find(word) != -1:
                check = 1
        except:
            print('error')
    return check

def block_the_blue(driver, verified_accounts):
    url_template = 'https://twitter.com/{}'
    for account in verified_accounts:
        try:
            url = url_template.format(account)
            driver.get(url)
            time.sleep(2)
            guilty = the_scales_of_justice(driver)
            if guilty == 1:
                button = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='userActions']")))
                button.click()
                block = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='block']")))
                block.click()
                yes_i_definitely_want_to_block = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='confirmationSheetConfirm']")))
                yes_i_definitely_want_to_block.click()
            time.sleep(2)
        except:
            print("error")

def confirmations(verified_accounts):
    verified_accounts_string = ", ".join(verified_accounts)
    return_string = f"Users up for blocking: {verified_accounts_string}"
    print(return_string)
    proceed = input("Proceed (Y or N)?  ")
    if proceed == "N":
        print("Blocking canceled...")
        sys.exit()
    return
