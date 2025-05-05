import json
import os
import time
from urllib.parse import urljoin

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


load_dotenv()


COOKIES_FILE = "app/cookies.json"
DJINNI_URL = "https://djinni.co"

DJINNI_EMAIL = os.getenv("DJINNI_EMAIL")
DJINNI_PASSWORD = os.getenv("DJINNI_PASSWORD")


def save_cookies(driver, path):
    cookies = driver.get_cookies()
    with open(path, "w") as file:
        json.dump(cookies, file, indent=2)


def load_cookies(driver, path):
    with open(path, "r") as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)


def is_authenticated(driver):
    driver.get(DJINNI_URL + "/my/")
    time.sleep(3)
    return "login" not in driver.current_url.lower()


def start_driver(headless=False):
    chrome_options = Options()
    if headless:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    return driver


def authenticate():
    driver = start_driver(headless=True)
    login_url = urljoin(DJINNI_URL, "login")
    driver.get(login_url)

    try:
        wait = WebDriverWait(driver, 10)
        print("Current URL:", driver.current_url)

        email_input = wait.until(
            EC.visibility_of_element_located((By.ID, "email"))
            )
        password_input = driver.find_element(By.ID, "password")

        email_input.send_keys(DJINNI_EMAIL)
        password_input.send_keys(DJINNI_PASSWORD)
        password_input.send_keys(Keys.RETURN)

        wait.until(lambda d: "/my/" in d.current_url)

        print("Успішний логін")

    except Exception as e:
        print("Login failed:", e)
        driver.quit()
        raise

    save_cookies(driver, COOKIES_FILE)
    return driver
