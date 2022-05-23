from time import sleep
from selenium import webdriver
from os.path import abspath
from selenium.webdriver.chrome import options
import yaml
import argparse
import atexit

browser = None
min_sleep_time = 1

def login_flow(username: str, password: str):
    # Login to Instagram using the Selenium browser
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

def update_config(config_path: str, config: dict):
    # Update the config file with the config without the used post
    with open(config_path, 'w') as config_file:
        yaml.safe_dump(config, config_file)

def open_browser():
    # Setup and open the Firefox browser
    global browser
    opts = webdriver.FirefoxOptions()
    opts.add_argument("--headless")
    opts.add_argument("--profile=/path/to/snap/firefox/common/.mozilla/firefox/filename.default-release")
    browser = webdriver.Firefox(options=opts)
    browser.implicitly_wait(5)
    browser.get('https://www.instagram.com/')

def parse_arguments():
    # Parse the arguments
    parser = argparse.ArgumentParser(description='Instagram Bot')
    parser.add_argument('-c', '--config', help='Config file', required=True)
    return parser.parse_args()

def select_photo_add_post(new_post_selector: str, button_selector: str, caption_selector: str, content: dict):
    # Select the new post button
    new_post_button = browser.find_element_by_css_selector(f"button[class='{new_post_selector}']")
    new_post_button.click()

    # Upload the picture
    fileInput = browser.find_element_by_css_selector("input[type='file']")
    fileInput.send_keys(abspath(content['image_path']))

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
    caption_input.send_keys(content.get('caption', ''))

    sleep(min_sleep_time)

    # Click the share button
    possible_buttons = browser.find_elements_by_css_selector(f"button[class='{button_selector}']")
    for button in possible_buttons:
        if button.text == 'Share':
            button.click()
            break

    sleep(min_sleep_time)

def exit_handler():
    browser.quit()

if __name__ == '__main__':

    # parse the arguments
    args = parse_arguments()

    # load settings
    config = load_config(args.config)

    # exit if there's nothing to post
    if (len(config['posts']) == 0):
        print('Nothing to post')
        exit(0)

    # open browser
    open_browser()

    # register exit handler
    atexit.register(exit_handler)

    # login to Instagram
    login_flow(config['username'], config['password'])

    sleep(min_sleep_time)

    # remove the entry used for this run
    post = config['posts'].pop(0)

    # select and upload the photo with caption
    select_photo_add_post(config.get('new-post-selector'), config.get('button-selector'), config.get('caption-selector'), post)

    # update config file
    update_config(args.config, config)

    sleep(min_sleep_time)

    # closer browser
    exit_handler()
