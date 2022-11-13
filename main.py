from selenium import webdriver
from selenium.webdriver.common.by import By
from random import randint
from math import floor
import time
import config

def wait(seconds = 1):
    time.sleep(seconds)

def login(mail, password):
    login_mail_input = driver.find_element(By.NAME, "email")
    login_password_input = driver.find_element(By.NAME, "password")
    login_submit = driver.find_element(By.XPATH, "//input[@type='submit']")

    login_mail_input.send_keys(mail)
    login_password_input.send_keys(password)
    login_submit.click()    

def vote():
    # Calculate scores beforehand (will be reset every time vote() is called)
    # Return an array with each score : [smart, trust, attract]
    attractMod = 0.85
    scores = calculateScores(attractMod)

    for i in range(0,3):
        # Smart / Trust / Attract
        score_buttons = score_columns[i].find_elements(By.CLASS_NAME, "score-value")

        for b in score_buttons:
            if b.text == scores[i]:
                wait(round(randint(300,4000)/1000, 1)) # rand value can't be set by default, otherwise it is resolved only once when the script is initiated
                b.click()
    wait(round(randint(300,4000)/1000, 1))
    vote_button.click()

def calculateScores(attractMod):
    attractScore = floor(randint(1, 100) * attractMod / 25)

    match attractScore:
        case 0:
            trustScore = floor(randint(1, 55) / 25) # if attractiveness is 0, trustworthiness can't be higher than 2 and frequently below 2
            smartScore = floor(randint(1, 55) / 25) 
        case 1:
            trustScore = floor(randint(20, 80) / 25) # if attractiveness is 1, trustworthiness is rarely 0, and rarely 3
            smartScore = floor(randint(20, 80) / 25)
        case 2:
            trustScore = floor(randint(25, 100) / 25) # if attractiveness is 2, trustworthiness can't be lower than 1
            smartScore = floor(randint(25, 100) / 25) 
        case 3:
            trustScore = floor(randint(45, 100) / 25) # if attractiveness is 3, trustworthiness is never below 1, rarely below 2
            smartScore = floor(randint(45, 100) / 25) 
    
    return list(map(str, [smartScore, trustScore, attractScore]))

driver = webdriver.Firefox(executable_path=config.geckodriver_path)
driver.get("https://www.photofeeler.com/vote/dating")

wait(2)

login(config.login, config.password)

wait(5)

score_columns = driver.find_elements(By.CLASS_NAME, "score-column")
del score_columns[0:3] # remove score-column elements that don't have a score-value class
vote_button = driver.find_element(By.CLASS_NAME, "vote-button")
karma_level = driver.find_element(By.CLASS_NAME, "karma-value")

while (karma_level.text != "Max"):
    vote()
    wait()
    karma_level = driver.find_element(By.CLASS_NAME, "karma-value")

wait()
driver.close()



