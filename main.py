from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from webdriver_manager.chrome import ChromeDriverManager
import json

# To not get rate-limited
cached = []

#webdriver options
options = Options()
options.add_experimental_option("detach", True)

def get_account() -> list[(str, str)]:
    """
    Gets a roblox account from api
    :return username, password:
    """
    data = requests.get("https://api.bloxalts.xyz/v1/generate/5").json()
    if data["status"] == 200:
        accounts = []
        for account in data["accounts"]:
            x = account.split(":")
            accounts.append((x[0], x[1]))
        return accounts
    elif data["status"] == 429:
        print("Rate-limited, waiting...")
        time.sleep(10)
        return get_account()
    else:
        print("Something went wrong, please notify the developer")
        quit()


def save_json(filename: str, data: list) -> None:
    """
    Saves a json file
    :param filename:
    :param data:
    :return:
    """
    with open(filename, "w") as f:
        json.dump(data, f)


def cache_worker() -> (str, str):
    """
    Caches the current account
    :return:
    """
    global cached
    if len(cached) == 0:
        cached = get_account()
        print("Cached new accounts")
    n = cached[-1]
    cached.pop(-1)
    save_json("accounts.json", cached)
    return n


def check_if_logged_in(driver) -> None:
    """
    Checks if the user is logged in and logouts if needed
    NOTE!!!
    NOT TESTED!!!
    ----------
    """

    if driver.current_url != "https://www.roblox.com/login":
        print("Probably already logged in, trying to logout, if this fails, please logout manually and notify the developer")
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".logout-menu-item"))))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".change-email-button"))))
        return
    else:
        return


def load_json(filename: str) -> dict:
    """
    Loads a json file
    :param filename:
    :return:
    """
    with open(filename, "r") as f:
        return json.load(f)


def login(username, password) -> None:
    """
    Logs in to roblox
    """
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    driver.get("https://www.roblox.com/login")
    time.sleep(1)
    check_if_logged_in(driver)
    driver.find_element(By.ID, "login-username").send_keys(username)
    driver.find_element(By.ID, "login-password").send_keys(password)
    driver.execute_script("arguments[0].click();", WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#login-button"))))

    print("Logged in as: " + username)
    # To do:
    # Skip the captcha if possible


if __name__ == '__main__':
    print("Made with love by NimVrod\nCredits to: Bloxalts for the API")
    try:
        cached = load_json("accounts.json")
        print("Loaded saved accounts")
    except FileNotFoundError:
        print("No accounts saved found.")
    while True:
        if input("Press 'g' to get a new account, press anything else to quit: ") == "g":
            account = cache_worker()
            login(account[0], account[1])
        else:
            break
    print("Be sure to star the repo on github if you like it!")
    quit()

