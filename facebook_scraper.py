# imports here
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
import time
import os

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
path_root_project = "/home/dsilva/www/college-extension-project"
# Specify the path to the ChromeDriver executable
service = Service(path_root_project + "/chromedriver")

# specify the path to chromedriver.exe (download and save on your computer)
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

data = {
    "livro_dos_espiritos": [],
    "evangelho_segundo_o_espiritismo": [],
}

storage_message = {
    "livro_dos_espiritos_message": [],
    "evangelho_segundo_o_espiritismo_message": [],
}

profile_name = "allan kardec"
reaction_selector = "div > span.xrbpyxo.x6ikm8r.x10wlt62.xlyipyv.x1exxlbk > span > span"
user_profile_selector = (
    "h2.html-h2 strong.html-strong span.html-span a span.xt0psk2 span"
)
n_scrolls = int(os.getenv("SCROLLS"))
for i in range(1, n_scrolls):
    # user_profile = driver.find_elements(By.CSS_SELECTOR, user_profile_selector)
    elements = driver.find_elements(
        By.CSS_SELECTOR, "[data-ad-comet-preview='message']"
    )
    message = ' '.join([div.text for div in elements])

    print("scroll - ", i)
    # if profile_name in user_profile[0].text.lower().strip():
    if (
        "livro dos espiritos" in message.lower().strip()
        or "livro dos espíritos" in message.lower().strip()
    ):
        if message.lower().strip() not in storage_message["livro_dos_espiritos_message"]:
            reaction_element = driver.find_elements(
                By.CSS_SELECTOR, reaction_selector
            )
            storage_message["livro_dos_espiritos_message"].extend(
                [message.lower().strip()]
            )

            data["livro_dos_espiritos"].extend([reaction_element[0].text])
            data["evangelho_segundo_o_espiritismo"].extend(
                ["0"]
            )  # Ensure same length
            

    elif "evangelho segundo o espiritismo" in message.lower().strip():
        if (
            message.lower().strip()
            not in storage_message["evangelho_segundo_o_espiritismo_message"]
        ):
            reaction_element = driver.find_elements(
                By.CSS_SELECTOR, reaction_selector
            )

            storage_message["evangelho_segundo_o_espiritismo_message"].extend(
                [message.lower().strip()]
            )
            data["evangelho_segundo_o_espiritismo"].extend(
                [reaction_element[0].text]
            )
            data["livro_dos_espiritos"].extend(["0"])  # Ensure same length
            

    else:
        print("Not found")
        data["livro_dos_espiritos"].extend(["0"])  # Ensure same length
        data["evangelho_segundo_o_espiritismo"].extend(["0"])  # Ensure same length

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

print(data)

df = pd.DataFrame(data)
# Check if data_scraped.csv file exists
if os.path.exists(path_root_project + "/datasource/data_scraped.csv"):
    # If file exists, delete it
    os.remove(path_root_project + "/datasource/data_scraped.csv")

# Save DataFrame to data_scraped.csv file
df.to_csv(path_root_project + "/datasource/data_scraped.csv", index=False)
