from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains 
import time

username = ""
password = ""

words_list = {}

words_file = open(r"slownik.txt", 'a+', encoding='utf-8')
for x in words_file:
    x_corrected = x.rstrip('\n')
    words_list[x_corrected.split(":")[0]] = x_corrected.split(":")[1]
words_file.close()

print(words_list)
#mutowanie zakładki
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--mute-audio")
#otwieranie chrome
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1200, 900)
#uruchomienie strony
driver.get("https://instaling.pl/")
assert "Insta.Ling" in driver.title
main_login_button = driver.find_element(By.CSS_SELECTOR, "a[class='btn navbar-profile p-0 m-0 pr-2']")
jebane_zgody = driver.find_element(By.CSS_SELECTOR, "p[class='fc-button-label']")
#klikniecie na przycisk zaloguj na stronie glownej
jebane_zgody.click()
time.sleep(1)
main_login_button.click()
time.sleep(1)
login_field = driver.find_element(By.ID, "log_email")
password_field = driver.find_element(By.ID, "log_password")
login_button = driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-primary w-100 mt-3 mb-3']")
login_field.send_keys(username)
password_field.send_keys(password)
#klikniecie na przycisk logowania
login_button.click()
time.sleep(1)
try:
    finish_session_button = driver.find_element(By.CSS_SELECTOR, "a[class='big_button btn btn-session sesion']")
except NoSuchElementException:
    finish_session_button = driver.find_element(By.CSS_SELECTOR, "a[class='big_button btn btn-session sesion blink_me']")
#klikniecie na przycisk dokonczenia sesji
finish_session_button.click()
time.sleep(1)
try:
    start_session_button = driver.find_element(By.CSS_SELECTOR, "div[id='start_session_button']")
    # klikniecie na przycisk rozpoczęcia sesji
    # ActionChains(driver).move_to_element(start_session_button).click().perform()
    start_session_button.click()
    time.sleep(1)
except ElementNotInteractableException:
    continue_session_button = driver.find_element(By.ID, "continue_session_button")
    # klikniecie na przycisk kontynuowania sesji
    continue_session_button.click()
    time.sleep(1)

while True:
    word = driver.find_element(By.CLASS_NAME, "translations").text
    print("Definicja = " + word)
    input_box = driver.find_element(By.ID, "answer")
    check_button = driver.find_element(By.ID, "check")
    if word in words_list:
        input_box.send_keys(words_list[word])
        check_button.click()
        time.sleep(1)
        next_word_button = driver.find_element(By.ID, "next_word")
        next_word_button.click()
        time.sleep(1)
    else:
        try:
            check_button.click()
        except ElementNotInteractableException:
            xnext = driver.find_element(By.ID, "know_new")
            try:
                xnext.click()
            except ElementNotInteractableException:
                break
            time.sleep(1)
            skip = driver.find_element(By.ID, "skip")
            skip.click()
            time.sleep(1)
            continue
        time.sleep(1)
        answer = driver.find_element(By.ID, "word").text
        print("Odpowiedz: " + answer)
        words_list[word] = answer
        words_file = open(r"slownik.txt", 'a+', encoding='utf-8')
        words_file.write("\n"+word+":"+answer)
        words_file.close()
        time.sleep(1)
        next_word_button = driver.find_element(By.ID, "next_word")
        next_word_button.click()
        time.sleep(1)
