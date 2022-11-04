from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import config

def login(mail, password):
    login_mail_input = driver.find_element(By.NAME, "email")
    login_password_input = driver.find_element(By.NAME, "password")
    login_submit = driver.find_element(By.XPATH, "//input[@type='submit']")

    login_mail_input.send_keys(mail)
    login_password_input.send_keys(password)
    login_submit.click()


driver = webdriver.Firefox(executable_path=config.geckodriver_path)
driver.get("https://www.photofeeler.com/vote/dating")

login(config.login, config.password)

# karma_gauge = driver.find_element(By.CSS_SELECTOR, "div.karma-bar")


# driver.close()



