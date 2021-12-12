from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import yaml
import argparse

browser = None
min_sleep_time = 1

def login_flow(username: str, password: str):
    # Login to Instagram
    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = browser.find_element_by_css_selector("button[type='submit']")
    login_button.click()
    sleep(5)

def load_config(config_path: str):
    # Load the config file
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def open_browser():
    # Setup and open the Firefox browser
    global browser
    browser = webdriver.Firefox()
    # browser.maximize_window()
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com/')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Instagram Bot')
    parser.add_argument('-c', '--config', help='Config file', required=False)
    return parser.parse_args()

def select_photo_add_post(new_post_selector: str, button_selector: str, caption_selector: str):
    # Select the new post button
    new_post_button = browser.find_element_by_css_selector(f"button[class='{new_post_selector}']")
    new_post_button.click()

    # Upload the picture
    fileInput = browser.find_element_by_css_selector("input[type='file']")
    # TODO Drive this through config.
    fileInput.send_keys('/path/to/image.jpg')

    # Wait for upload to finish
    sleep(2)

    for _ in range(0,2):
        possible_buttons = browser.find_elements_by_css_selector(f"button[class='{button_selector}']")
        for button in possible_buttons:
            if button.text == 'Next':
                button.click()
                break

    sleep(min_sleep_time)

    # Add a caption
    caption_input = browser.find_element_by_css_selector(f"textarea[class='{caption_selector}']")
    # TODO Drive this through config.
    caption_input.send_keys('This is a test! Built with Codex via Github Copilot.')

    sleep(min_sleep_time)

    # Click the share button
    possible_buttons = browser.find_elements_by_css_selector(f"button[class='{button_selector}']")
    for button in possible_buttons:
        if button.text == 'Share':
            button.click()
            break

    sleep(min_sleep_time)

if __name__ == '__main__':

    args = parse_arguments()

    # load settings
    config = load_config(args.config)

    # open browser
    open_browser()

    # login to Instagram
    login_flow(config['username'], config['password'])

    sleep(min_sleep_time)

    # select and upload the photo with caption
    select_photo_add_post(config.get('new-post-selector'), config.get('button-selector'), config.get('caption-selector'))

    sleep(min_sleep_time)

    # closer browser
    browser.close()