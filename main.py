from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from functions import handle_username_dupe, check_username_dupe, find_verified_users, scroll_page, remove_duplicates_from_list, block_the_blue, confirmations, guide, remove

import time

#TODO: Check for no bio, add way for users to supply words to ban list

boolean = True;
while boolean:
    function = guide(1)
    if(int(function) == 2):
        boolean2 = True
        while boolean2:
            pref = guide(2)
            if (int(pref) == 1):
                #TODO: Build out add words
                print('add')
                boolean2 = False
            elif (int(pref) == 2):
                new_text = ""
                with open('termslist.txt', 'r') as file:
                    text = file.read()
                    print(f"\nHere is a list of the terms you have saved:\n\n{text}\n\n")
                    text_list = text.split(", ")
                    remove_list = []
                    boolean3 = True
                    while boolean3:
                        word = remove(text_list)
                        if(word == "exit"):
                            boolean3 = False
                        elif(word != "error" and word != "next" and word not in remove_list):
                            remove_list.append(word)
                            print(f"\nSuccess! {word} will be deleted.\n")
                        elif(word in remove_list):
                            print(f"\n{word} has already been queued for deletion!\n")
                    for w in remove_list:
                        if w in text_list:
                            text_list.remove(w)
                    new_text = ", ".join(text_list)
                    print(f"\nnew text {new_text}")
                with open("termslist.txt", "w") as file:
                    file.write(new_text)
                deleted_string = ", ".join(remove_list)
                print(f"\nSuccess! The following words were deleted: {deleted_string}.\n")
                boolean2 = False
            else:
                print('Please enter 1 or 2!');
        boolean = False
    elif(int(function) == 1):
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
        boolean = False
    else:
        print("Please enter 1 or 2!")

print("Press enter to end script!")
input()