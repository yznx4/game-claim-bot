import os
import time
import random
import pickle
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()


def get_driver():
    options = webdriver.ChromeOptions()

    # Use same Chrome profile as Epic
    options.add_argument(r"--user-data-dir=C:\Users\YOUR_USERNAME\AppData\Local\Google\Chrome\User Data")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    return webdriver.Chrome(options=options)


def save_cookies(driver, path="steam_cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, path="steam_cookies.pkl"):
    try:
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("⚠️ No saved cookies found. Logging in manually...")


def claim_steam_game(url):
    driver = get_driver()
    try:
        driver.get("https://store.steampowered.com/")
        load_cookies(driver)
        driver.get(url)

        # Handle login if required
        if "login" in driver.current_url:
            print("🔑 Logging in...")
            driver.find_element(By.CLASS_NAME, "global_action_link").click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "input_username"))
            ).send_keys(os.getenv('STEAM_USER'))

            driver.find_element(By.ID, "input_password").send_keys(os.getenv('STEAM_PASSWORD'))
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            print("⚠️ Handle Steam Guard within 30 seconds...")
            time.sleep(30)

            if "login" in driver.current_url.lower():
                raise Exception("Login failed!")

            save_cookies(driver)

        # Claim the game
        claim_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@class='game_purchase_action']/a"))
        )

        # Human-like interaction
        time.sleep(random.uniform(1, 3))
        claim_button.click()
        print("✅ Steam: Claim successful!")

    except Exception as e:
        print(f"❌ Error: {e}")
        driver.save_screenshot("steam_error.png")
    finally:
        driver.quit()
