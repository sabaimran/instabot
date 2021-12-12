from time import sleep

from selenium import webdriver

import yaml

config = {}

def login_flow():
    # login
    username_input = browser.find_element_by_css_selector("input[name='username']")
    password_input = browser.find_element_by_css_selector("input[name='password']")

    username_input.send_keys(config['username'])
    password_input.send_keys(config['password'])

    login_button = browser.find_element_by_css_selector("button[type='submit']")
    login_button.click()
    sleep(5)

def load_config():
    global config
    with open('config.yml', 'r') as config_file:
        config = yaml.load(config_file)

if __name__ == '__main__':

    # load settings

    # open browser
    browser = webdriver.Firefox()
    browser.implicitly_wait(5)

    browser.get('https://www.instagram.com/')

    login_flow()

    sleep(5)

    # closer browser
    browser.close()