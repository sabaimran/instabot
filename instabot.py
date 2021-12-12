from time import sleep

from selenium import webdriver

import yaml

browser = None

def login_flow(username: str, password: str):
    # Login to Instagram
    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    username_input.send_keys(username)
    password_input.send_keys(password)

    login_button = browser.find_element_by_css_selector("button[type='submit']")
    login_button.click()
    sleep(5)

def load_config():
    # Load the config file
    global config
    with open('config.yml', 'r') as config_file:
        config = yaml.safe_load(config_file)

def open_browser():
    # Setup and open the Firefox browser
    global browser
    browser = webdriver.Firefox()
    browser.get('https://www.instagram.com/')

if __name__ == '__main__':

    # load settings
    config = load_config()

    # open browser
    open_browser()

    # login to Instagram
    login_flow(config['username'], config['password'])

    sleep(5)

    # closer browser
    browser.close()