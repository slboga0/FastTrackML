import os
import requests
from datetime import datetime, timedelta
import configparser
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def download_pdfs(username, password, base_url, download_folder, start_date, end_date):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)  # Explicit wait

    try:
        driver.get(base_url)  # Replace with the actual login URL
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        driver.delete_all_cookies()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        # Wait for successful login (adjust as needed)
        time.sleep(10)  # Can be replaced with explicit wait if needed

        for current_date in date_range(start_date, end_date):
            formatted_date = current_date.strftime("%Y-%m-%d")
            url = base_url.replace("date_placeholder", formatted_date)
            file_name = f"{formatted_date}.pdf"
            download_file(driver, url, download_folder, file_name, wait)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

def download_file(driver, url, download_folder, file_name, wait):
    try:
        driver.get(url)

        # Improved download waiting (using expected conditions)
        # Check if the file exists in the directory after a reasonable time.
        # This is a more robust way to handle downloads.
        timeout = 30  # Maximum wait time in seconds
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(os.path.join(download_folder, file_name)):
                print(f"File downloaded to {download_folder}/{file_name}")
                return #Exit the function when the file is downloaded

            time.sleep(1)  # Check every second

        print(f"Timeout waiting for download: {url}") #Print message if download fails after timeout
        
        page_source = driver.page_source
        if "Error!" in page_source:
             print(f"Download authorization error occurred for: {url}")

    except Exception as e:
        print(f"An error occurred while downloading {url}: {e}")

def date_range(start_date, end_date):
    current_date = start_date
    while current_date <= end_date:
        yield current_date
        current_date += timedelta(days=1)

def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, '..', 'config.ini')
    config = load_config(config_file_path)

    base_url = config["DEFAULT"].get("base_url", "https://www.example.com/product/download/2024-12-01/DRM/USA/TB/GP/D/0/")
    download_folder = config["DEFAULT"]["folder_path"]
    start_date = datetime.strptime(config["DEFAULT"]["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(config["DEFAULT"]["end_date"], "%Y-%m-%d")
    username = config["DEFAULT"]["user_name"]
    password = config["DEFAULT"]["password"]

    download_pdfs(username, password, base_url, download_folder, start_date, end_date)