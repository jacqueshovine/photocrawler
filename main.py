from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
from math import floor
import time
import random
import config

options = Options()
options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver = webdriver.Firefox(options=options)

def wait(min_seconds=1, max_seconds=5):
    wait_time = round(random.uniform(min_seconds, max_seconds), 1)
    time.sleep(wait_time)

def login(mail, password):
    if (driver.current_url != "https://www.photofeeler.com/vote/dating"):
        login_mail_input = driver.find_element(By.NAME, "email")
        login_password_input = driver.find_element(By.NAME, "password")
        login_submit = driver.find_element(By.XPATH, "//input[@type='submit']")

        login_mail_input.send_keys(mail)
        login_password_input.send_keys(password)
        login_submit.click()

def move_mouse_around_photo(photo_element):
    actions = ActionChains(driver)
    actions.move_to_element(photo_element).perform()
    wait(2, 4)  # Simulate looking at the photo
    for _ in range(3):
        offset_x = random.randint(-20, 20)
        offset_y = random.randint(-20, 20)
        actions.move_to_element_with_offset(photo_element, offset_x, offset_y).perform()
        wait(1)

def handle_suggestions():
    suggestions = driver.find_elements(By.CSS_SELECTOR, ".tab-pane.active > .note-button-row > .btn")  # Replace with actual CSS selector

    filtered_suggestions = [s for s in suggestions if s.text.strip()]

    if random.random() < 0.05:  # 5% chance to click a suggestion
        random_index = random.randint(1, len(filtered_suggestions) - 1) # Skip the first suggestion as it's the "custom" and needs additional input
        suggestion = filtered_suggestions[random_index]

        actions = ActionChains(driver)
        actions.move_to_element(suggestion).perform()
        wait(round(random.randint(300, 900) / 1000, 1))  # Simulate hovering time
        print(f"Clicking suggestion: {suggestion.text}")
        suggestion.click()

def vote():
    # Calculate scores beforehand (will be reset every time vote() is called)
    # Return an array with each score : [smart, trust, attract]
    attractMod = 0.85
    scores = calculateScores(attractMod)

    photo_element = driver.find_element(By.CLASS_NAME, "photo-container")
    move_mouse_around_photo(photo_element)

    score_columns = driver.find_elements(By.CLASS_NAME, "score-column")
    del score_columns[0:3] # remove score-column elements that don't have a score-value class
    vote_button = driver.find_element(By.CLASS_NAME, "vote-button")

    random.shuffle(score_columns)

    for i, score_column in enumerate(score_columns):
        score_buttons = score_column.find_elements(By.CLASS_NAME, "score-value")
        selected_score = scores[i]

        for b in score_buttons:
            if b.text == selected_score:
                wait(round(random.randint(300, 2500) / 1000, 1))
                actions = ActionChains(driver)
                actions.move_to_element(b).perform()
                wait(round(random.randint(300, 900) / 1000, 1))
                b.click()
                break

    wait(round(random.randint(300, 800) / 1000, 1))
    handle_suggestions()
    wait(round(random.randint(300, 1100) / 1000, 1))
    vote_button.click()

def calculateScores(attractMod):
    attractScore = floor(random.randint(1, 100) * attractMod / 25)

    match attractScore:
        case 0:
            trustScore = floor(random.randint(1, 55) / 25) # if attractiveness is 0, trustworthiness can't be higher than 2 and frequently below 2
            smartScore = floor(random.randint(1, 55) / 25) 
        case 1:
            trustScore = floor(random.randint(20, 80) / 25) # if attractiveness is 1, trustworthiness is rarely 0, and rarely 3
            smartScore = floor(random.randint(20, 80) / 25)
        case 2:
            trustScore = floor(random.randint(25, 100) / 25) # if attractiveness is 2, trustworthiness can't be lower than 1
            smartScore = floor(random.randint(25, 100) / 25) 
        case 3:
            trustScore = floor(random.randint(45, 100) / 25) # if attractiveness is 3, trustworthiness is never below 1, rarely below 2
            smartScore = floor(random.randint(45, 100) / 25) 
    
    return list(map(str, [smartScore, trustScore, attractScore]))

driver = webdriver.Firefox(executable_path=config.geckodriver_path)
driver.get("https://www.photofeeler.com/vote/dating")

wait(2)

login(config.login, config.password)

wait(3)

karma_level = driver.find_element(By.CLASS_NAME, "karma-value")

while (karma_level.text != "Max"):
    vote()
    wait()
    karma_level = driver.find_element(By.CLASS_NAME, "karma-value")

wait()
driver.close()



