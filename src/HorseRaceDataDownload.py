import logging
import os
import time
import configparser
import zipfile
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_track_filename(track_name, date_string=None):
    """Creates a filename in the format "trackname-MMDD.zip".

    Args:
        track_name: The name of the track.
        date_string: A date string in "YYYY-MM-DD" format. If None, uses the current date.

    Returns:
        A string representing the filename, or None if the date string is invalid.
    """
    if date_string is None:
        date_obj = datetime.now().date()
    else:
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date string format. Use YYYY-MM-DD.")
            return None

    month_day_str = date_obj.strftime("%m%d")
    archive_suffix = f"{month_day_str}{'k'}.zip"
    return f"{track_name}{archive_suffix}"

def get_track_result_filename(track_name, date_string=None):
    """Creates a filename in the format "trackname-MMDD.zip".

    Args:
        track_name: The name of the track.
        date_string: A date string in "YYYY-MM-DD" format. If None, uses the current date.

    Returns:
        A string representing the filename, or None if the date string is invalid.
    """
    if date_string is None:
        date_obj = datetime.now().date()
    else:
        try:
            date_obj = datetime.strptime(date_string, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date string format. Use YYYY-MM-DD.")
            return None

    month_day_str = date_obj.strftime("%m%d")
    archive_suffix = f"{month_day_str}{'d'}.zip"
    return f"{track_name}{archive_suffix}"

def download_pdfs(username, password, base_url, login_url, download_folder, start_date, end_date, result=False):
    options = webdriver.ChromeOptions()
    prefs = {"download.default_directory": download_folder}
    options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    wait = WebDriverWait(driver, 20)  # Explicit wait

    try:
        driver.get(login_url)  # Replace with the actual login URL
        username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
        password_field = driver.find_element(By.ID, 'password')
        login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')

        driver.delete_all_cookies()
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        # Wait for successful login (adjust as needed)
        time.sleep(3)  # Can be replaced with explicit wait if needed

        for current_date in date_range(start_date, end_date):
            formatted_date = current_date.strftime("%Y-%m-%d")
            url = base_url.replace("date_placeholder", formatted_date)
            file_name = get_track_result_filename("sax", formatted_date)

            if os.path.exists(os.path.join(download_folder, file_name)):
                print(f"File '{file_name}' already exists at '{file_name}'. Skipping download.")
            else:
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

        time.sleep(5)  # Check every second

        if os.path.exists(os.path.join(download_folder, file_name)):
            print(f"File downloaded to {download_folder}/{file_name}")
            return #Exit the function when the file is downloaded

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

def unzip_files(source_folder, destination_folder, archive_folder, replace_files=False):
    """Unzip all files in the source folder directly into the destination folder, move zipped files to an archive folder.

    Args:
        source_folder (str): Path to the folder containing zip files.
        destination_folder (str): Path to the folder where files will be extracted.
        archive_folder (str): Path to the folder where zip files will be moved after extraction.
        replace_files (bool): If True, replace existing files in the destination folder.
    """
    for file_name in os.listdir(source_folder):
        file_path = os.path.join(source_folder, file_name)

        if zipfile.is_zipfile(file_path):
            try:
                # Unzip the file
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    for member in zip_ref.namelist():
                        # Extract only the file name to the destination folder
                        extracted_file_name = os.path.basename(member)
                        destination_file_path = os.path.join(destination_folder, extracted_file_name)

                        if os.path.exists(destination_file_path) and not replace_files:
                            logging.info(f"File already exists and replace_files is False: {destination_file_path}")
                            continue

                        # Write the file to the destination folder
                        with open(destination_file_path, 'wb') as f:
                            f.write(zip_ref.read(member))

                logging.info(f"Unzipped: {file_name}")

                # Move the zip file to the archive folder
                os.makedirs(archive_folder, exist_ok=True)
                archived_path = os.path.join(archive_folder, file_name)
                os.rename(file_path, archived_path)

                logging.info(f"Moved to archive: {file_name}")

            except Exception as e:
                logging.error(f"Failed to unzip {file_name}: {e}")


def download_past_performance_files(result=False):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_file_path = os.path.join(script_dir, '..', 'config.ini')

    print(f"Script directory: {script_dir}")  # Print the script's directory
    print(f"Config file path: {config_file_path}")  # Print the constructed path

    # Check if the file exists:
    if os.path.exists(config_file_path):
        print("Config file exists!")
    else:
        print("Config file DOES NOT EXIST at the specified path!")

    config = configparser.ConfigParser()
    config.read(config_file_path)

    login_url = config["DEFAULT"].get("login_url", "https://www.brisnet.com/product/login")
    base_url = config["DEFAULT"].get("base_url", "https://www.example.com/product/download/2024-12-01/DRM/USA/TB/GP/D/0/")
    result_url = config["DEFAULT"].get("result_url", "https://www.example.com/product/download/2024-12-01/IRX/USA/TB/GP/D/0/")
    pp_download_folder = config["DEFAULT"]["folder_path"]
    results_download_folder = config["DEFAULT"]["results_p"]
    start_date = datetime.strptime(config["DEFAULT"]["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(config["DEFAULT"]["end_date"], "%Y-%m-%d")
    username = config["DEFAULT"]["user_name"]
    password = config["DEFAULT"]["password"]

    if (result == False):
        download_pdfs(username, password, base_url, login_url, pp_download_folder, start_date, end_date)
    else:
        download_pdfs(username, password, result_url, login_url, results_download_folder, start_date, end_date, result=True)

if __name__ == "__main__":
    
    utility = "PP"
    source_folder = r"C:\Users\SamBo\Projects\FastTrackML\data\raw\results"
    destination_folder = r"C:\Users\SamBo\Projects\FastTrackML\data\raw\results"
    archive_folder = r"C:\Users\SamBo\Projects\FastTrackML\data\raw\results\archive"
    #utility = "zip"
    #utility = "result"

    if (utility == "pp"):
        download_past_performance_files(result=False)
    elif (utility == "zip"):
        # Unzip files
        unzip_files(source_folder, destination_folder, archive_folder, replace_files=True)
    else:
        download_past_performance_files(result=True)