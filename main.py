from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
import time
import config

def wait(seconds = round(randint(300,1000)/1000, 1)):
    time.sleep(seconds)

def login(mail, password):
    login_mail_input = driver.find_element(By.NAME, "email")
    login_password_input = driver.find_element(By.NAME, "password")
    login_submit = driver.find_element(By.XPATH, "//input[@type='submit']")

    login_mail_input.send_keys(mail)
    login_password_input.send_keys(password)
    login_submit.click()    

def vote():
    for col in score_columns:
        score_buttons = col.find_elements(By.CLASS_NAME, "score-value")
        score = str(randint(0,3)) # Python has no ===, must parse as a string for comparison
        for b in score_buttons:
            if b.text == score:
                wait() # sleep between O.3 and 1 second
                b.click()
    wait()
    vote_button.click()

driver = webdriver.Firefox(executable_path=config.geckodriver_path)
driver.get("https://www.photofeeler.com/vote/dating")

wait(2)

login(config.login, config.password)

wait(2)

score_columns = driver.find_elements(By.CLASS_NAME, "score-column")
vote_button = driver.find_element(By.CLASS_NAME, "vote-button")

karma_level = driver.find_element(By.CLASS_NAME, "karma-label")

while (karma_level.text != "Max"):
    print(karma_level.text)
    vote()
    wait(1)
    karma_level = driver.find_element(By.CLASS_NAME, "karma-label")



# @@@@@@@@@@@@@@@@@@@@@ TESTING @@@@@@@@@@@@@@@@@@@@@@@@

# while 1:
#     time.sleep(round(randint(300,1000)/1000, 1))
#     print(round(randint(300,1000)/1000, 1))
#     print("ok")

# driver.get("https://laravel.com/docs/9.x/installation")

# divmain = driver.find_element(By.ID, "main-content")
# h1 = divmain.find_element(By.TAG_NAME, "h1")

# print(h1.text)

# karma_gauge = driver.find_element(By.CSS_SELECTOR, "div.karma-bar")

# @@@@@@@@@@@@@@@@@@@@@ END TESTING @@@@@@@@@@@@@@@@@@@@@

# driver.close()



