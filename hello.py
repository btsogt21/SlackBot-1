from datetime import datetime, timedelta
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as BS
import hashlib
import traceback

seen_hashes = set()

def reset_log():
    try:
        with open("Logs/reset_date.txt", "r") as reset_file:
            last_reset_date = datetime.strptime(reset_file.read().strip(), "%Y-%m-%d")
            if datetime.now() - last_reset_date > timedelta(days = 7):
                with open("Logs/hashes_log.txt", "w") as log_file:
                    log_file.write("")
                with open("Logs/reset_date.txt", "w") as reset_file:
                    reset_file.write(datetime.now().strftime("%Y-%m-%d"))
    except (FileNotFoundError, ValueError):
        # if file is not found or if the date is not in the correct format, create a new file
        with open("Logs/reset_date.txt", "w") as reset_file:
            reset_file.write(datetime.now().strftime("%Y-%m-%d"))

def load_hashes():
    try:
        with open("Logs/hashes_log.txt", "r") as log_file:
            return_set = set(line.split('_')[2] for line in log_file.read().splitlines())
            return return_set
    except FileNotFoundError:
        # return empty set if file is not found
        return set()

def hash_message(content):
    return hashlib.sha256(content.encode()).hexdigest()

def initialize_webdriver():
    chrome_driver_path = input("Enter the path to ChromeDriver: ")
    chrome_binary_path = input("Enter the path to the Chrome browser executable: ")
    # chrome_driver_path = "/usr/local/bin/chromedriver"
    # chrome_binary_path = "/Applications/GoogleChromeForTesting.app/Contents/MacOS/Google Chrome for Testing"
    options_ = Options()
    options_.binary_location = chrome_binary_path
    driver = webdriver.Chrome(service=Service(chrome_driver_path), options = options_)
    return driver

def navigate_to_slack_login(driver):
    driver.get("https://slack.com/signin")
    input("Please log in manually and then press Enter to continue...")
    print("Continuing script...")

def save_source(driver):
    with open("source.html", "w") as html_file:
        html_file.write(driver.page_source)
    
def collect_code(driver):
    # driver.switch_to.window(driver.current_window_handle)
    button_clicked = False
    try:
        print("Collecting code...")
        scrape_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") # get current time for filebts name
        print(f"Scraping at {scrape_time}...")
        all_messages = driver.find_elements(By.CLASS_NAME, 'c-virtual_list__item')
        # retrieve the last 5 messages
        for message in all_messages[-5:]:
            message_html = message.get_attribute('outerHTML')
            soup = BS(message_html, 'html.parser')
            message_text = soup.get_text(separator = ' ')
            message_hash = hash_message(message_text)
            #check if the message has been seen before
            if message_hash not in seen_hashes:
                print(f"New or changed message found at {scrape_time}. Hash: {message_hash}")
                with open(f"Logs/hashes_log.txt", "a") as log_file:
                    log_file.write(f"{scrape_time}_{message_hash}\n")
                seen_hashes.add(message_hash)
            try:
                if 'Teaching Assistant' in message_text and "clicked  Claim This Shift" not in message_text:
                    print("found unclaimed TA shift")
                    print(message_text)
                    button_found = False
                    # maybe find a way to refactor everything from the try block immediately next
                    # to the final 'if button_found' block. (Commented 1:27 PM EST on 11/15/2023)
                    try:
                        found_button = message.find_element(By.CLASS_NAME, '-button--outline')
                        print('found on first try')
                        button_found = True
                    except:
                        print('could not find button on first try')
                    if not button_found:
                        try:
                            found_button = message.find_element(By.CLASS_NAME, 'c-button--outline')
                            # if found_button:
                            print('found on second try')
                            button_found = True
                        except:
                            print('could not find button on second try')
                    if not button_found:
                        try:
                            found_button = message.find_element(By.CLASS_NAME, 'c-button')
                            # if found_button:
                            print('found on third try')
                            button_found = True
                        except:
                            print('could not find button on third try')
                    if not button_found:
                        try:
                            found_button = message.find_element(By.CLASS_NAME, 'c-button--small')
                            # if found_button:
                            print('found on fourth try')
                            button_found = True
                        except:
                            print('could not find button on fourth try')
                    if not button_found:
                        try:
                            found_button = message.find_element(By.XPATH, './/button[contains(text(), "Claim This Shift")]')
                            # if found_button:
                            print('found on fifth try')
                            button_found = True
                        except:
                            print('could not find button on fifth try')
                    if button_found:
                        try:
                            found_button.click()
                            button_clicked = True
                        except:
                            print("Button found but could not be clicked")
            except:
                print("Some error, debug later")
                traceback.print_exc()
            # if 'Instructor - must be instructor-qualified' in message_html and "clicked Claim This Shift" not in message_html:
            #     print("found unclaimed instructor shift")
            #     button_found = False
            #     try:
            #         found_button = message.find_element(By.CLASS_NAME, '-button--outline')
            #         print('found on first try')
            #         button_found = True
            #     except:
            #         print('could not find button on first try')
            #     if not button_found:
            #         try:
            #             found_button = message.find_element(By.CLASS_NAME, 'c-button--outline')
            #             # if found_button:
            #             print('found on second try')
            #             button_found = True
            #         except:
            #             print('could not find button on second try')
            #     if not button_found:
            #         try:
            #             found_button = message.find_element(By.CLASS_NAME, 'c-button')
            #              # if found_button:
            #             print('found on third try')
            #             button_found = True
            #         except:
            #             print('could not find button on third try')
            #     if not button_found:
            #         try:
            #             found_button = message.find_element(By.CLASS_NAME, 'c-button--small')
            #             # if found_button:
            #             print('found on fourth try')
            #             button_found = True
            #         except:
            #             print('could not find button on fourth try')
            #     if not button_found:
            #         try:
            #             found_button = message.find_element(By.XPATH, './/button[contains(text(), "Claim This Shift")]')
            #             # if found_button:
            #             print('found on fifth try')
            #             button_found = True
            #         except:
            #             print('could not find button on fifth try')
            #     print('pause')
            #     time.sleep(1000)
    except Exception as e:
        print(f"An error has occurred {e}")
        traceback.print_exc()
    return button_clicked


def main():
    driver_1 = initialize_webdriver()
    reset_log()
    global seen_hashes
    seen_hashes = load_hashes()
    navigate_to_slack_login(driver_1)
    input("Please navigate to the test channel and then press Enter to continue...")
    while True:
        if collect_code(driver_1):
            print('button clicked, exiting script')
            break
        else:
            time.sleep(2)


if __name__ == "__main__":
    main()