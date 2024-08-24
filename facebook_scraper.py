# imports here
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import time

from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

# Step 1: Disable Alerts/Notifications
# !! Using code by pythonjar of Stackoverflow !!
# Please visit this thread for more details:
# https://stackoverflow.com/questions/41400934/handle-notifications-in-python-selenium-chrome-webdriver

# code by pythonjar, not me
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Step 2: Log into your personal Facebook account
# MAKE SURE to replace my_username and my_password with your own unique values
path_root_project = os.getenv("PATH_ROOT_PROJECT")
# Specify the path to the ChromeDriver executable
service = Service(path_root_project + "/chromedriver")

# specify the path to chromedriver (download and save on your computer)
driver = webdriver.Chrome(
    service=service,
    options=chrome_options,
)

driver.set_window_position(0, 0)
driver.maximize_window()

# open the webpage
driver.get("https://www.facebook.com")

# target username
username = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']"))
)
password = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']"))
)

# enter username and password
username.clear()
username.send_keys(os.getenv("FACEBOOK_EMAIL"))
password.clear()
password.send_keys(os.getenv("FACEBOOK_PASSWORD"))

# target the login button and click it
button = (
    WebDriverWait(driver, 2)
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']")))
    .click()
)

# We are logged in!
print("We are logged in!")

time.sleep(2)

# navigate to the profile of the user we want to scrape
driver.get(os.getenv("FACEBOOK_PROFILE"))

time.sleep(2)

key1 = "livro_dos_espiritos"
key2 = "evangelho_segundo_o_espiritismo"

empty = "0"

data = {
    key1: [],
    key2: [],
}

storage_message = {
    "livro_dos_espiritos_message": [],
    "evangelho_segundo_o_espiritismo_message": [],
}

reaction_selector = "div > span.xrbpyxo.x6ikm8r.x10wlt62.xlyipyv.x1exxlbk > span > span"
user_profile_selector = (
    "h2.html-h2 strong.html-strong span.html-span a span.xt0psk2 span"
)


def sanitize_data(data):
    if len(data[key1]) == len(data[key2]):
        for i in range(len(data[key1])):
            if i < len(data[key1]):
                if data[key1][i] == empty and data[key2][i] == empty:
                    del data[key1][i]
                    del data[key2][i]


def write_this(data, file_name):
    df = pd.DataFrame(data)
    # Check if data_scraped.csv file exists
    if os.path.exists(path_root_project + "/datasource/" + file_name):
        # If file exists, delete it
        os.remove(path_root_project + "/datasource/" + file_name)

    # Save DataFrame to data_scraped.csv file
    df.to_csv(path_root_project + "/datasource/" + file_name, index=False)


def write_data(data):
    sanitize_data(data)

    write_this(data, "data_scraped.csv")


def get_reaction_count():
    reaction_element = driver.find_elements(By.CSS_SELECTOR, reaction_selector)
    reaction_count = reaction_element[0].text.strip()
    reaction_count = reaction_count if reaction_count else empty
    return reaction_count


def write_reaction_count(k1, v1, k2, v2):
    data[k1].extend([v1])
    data[k2].extend([v2])  # Ensure same length
    write_data(data)


def write_message(key, msg):
    storage_message[key].extend([msg])


def get_messages():
    elements = driver.find_elements(
        By.CSS_SELECTOR, "[data-ad-comet-preview='message']"
    )
    message = ""
    for div in elements:
        try:
            message += div.text + " "
        except StaleElementReferenceException:
            continue
    message = message.lower().strip()
    return message


n_scrolls = int(os.getenv("SCROLLS"))
for i in range(1, n_scrolls):
    message = get_messages()

    print("scroll - ", i)

    if "livro dos espiritos" in message or "livro dos espíritos" in message:
        if message not in storage_message["livro_dos_espiritos_message"]:
            write_message("livro_dos_espiritos_message", message)
            write_reaction_count(key1, get_reaction_count(), key2, empty)

    elif "evangelho segundo o espiritismo" in message or "evangelho" in message:
        if message not in storage_message["evangelho_segundo_o_espiritismo_message"]:
            write_message("evangelho_segundo_o_espiritismo_message", message)
            write_reaction_count(key1, empty, key2, get_reaction_count())

    else:
        print("Not found")
        write_reaction_count(key1, empty, key2, empty)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

driver.quit()
