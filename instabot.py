from time import sleep
from selenium import webdriver
import yaml
import argparse

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

def load_config(config_path: str):
    # Load the config file
    with open(config_path, 'r') as config_file:
        return yaml.safe_load(config_file)

def open_browser():
    # Setup and open the Firefox browser
    global browser
    browser = webdriver.Firefox()
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com/')

def parse_arguments():
    parser = argparse.ArgumentParser(description='Instagram Bot')
    parser.add_argument('-c', '--config', help='Config file', required=False)
    return parser.parse_args()

def select_new_post_button():
    # Select the new post button
    new_post_button = browser.find_element_by_css_selector("button[class='wpO6b ZQScA ']")
    new_post_button.click()

if __name__ == '__main__':

    args = parse_arguments()

    # load settings
    config = load_config(args.config)

    # open browser
    open_browser()

    # login to Instagram
    login_flow(config['username'], config['password'])

    sleep(5)

    select_new_post_button()

    sleep(5)

    # closer browser
    browser.close()