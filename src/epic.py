import os
import time
import random
import pickle
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run without opening a window
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(options=options)


def save_cookies(driver, path="epic_cookies.pkl"):
    with open(path, "wb") as file:
        pickle.dump(driver.get_cookies(), file)


def load_cookies(driver, path="epic_cookies.pkl"):
    try:
        with open(path, "rb") as file:
            cookies = pickle.load(file)
            for cookie in cookies:
                driver.add_cookie(cookie)
    except FileNotFoundError:
        print("⚠️ No saved cookies found. Logging in manually...")


def claim_epic_game(url):
    driver = get_driver()
    try:
        driver.get("https://www.epicgames.com/store")
        load_cookies(driver)
        driver.get(url)  # Reload with cookies

        # Handle login if required
        if "login" in driver.current_url:
            print("🔑 Logging in...")
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(os.getenv('EPIC_EMAIL'))

            driver.find_element(By.ID, "password").send_keys(os.getenv('EPIC_PASSWORD'))
            driver.find_element(By.ID, "login-button").click()

            # Wait for manual 2FA
            print("⚠️ Complete 2FA within 30 seconds...")
            time.sleep(30)

            if "login" in driver.current_url.lower():
                raise Exception("Login failed!")

            save_cookies(driver)

        # Claim the game
        get_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Get')]"))
        )

        # Human-like interaction
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", get_button)
        time.sleep(random.uniform(1, 3))
        get_button.click()

        # Handle purchase confirmation
        place_order_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Place Order')]"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", place_order_button)
        time.sleep(random.uniform(1, 3))
        place_order_button.click()

        print("✅ Epic Games: Claim successful!")

    except Exception as e:
        print(f"❌ Error: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("epic_error.png")
    finally:
        driver.quit()
