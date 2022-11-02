from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import config

driver = webdriver.Firefox(executable_path=config.geckodriver_path)
driver.get("http://www.python.org")