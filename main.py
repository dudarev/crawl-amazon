import random
import re
import sys

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from credentials import AMAZON_EMAIL, AMAZON_PASSWORD

from bs4 import BeautifulSoup


# config parameters

RUN_AS_HEADLESS = True

SIGNIN_URL = \
    "https://www.amazon.com/gp/navigation/redirector.html/" + \
    "ref=sign-in-redirect?ie=UTF8&associationHandle=usflex&" + \
    "currentPageURL=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&" + \
    "pageType=Gateway&switchAccount=&" + \
    "yshURL=https%3A%2F%2Fwww.amazon.com%2Fgp%2F" + \
    "yourstore%2Fhome%3Fie%3DUTF8%26ref_%3Dnav_signin"

AVERAGE_RANDOM_WAIT_TIME = 1

SKIP_SPONSORED = False


def random_wait(driver):
    """
    Adds some random wait to emulate human behavior
    """
    driver.implicitly_wait(2 * AVERAGE_RANDOM_WAIT_TIME * random.random())


def init_driver():
    """
    Sets up Selenium webdriver

    Uses global `RUN_AS_HEADLESS` parameter.
    It's useful for testing to set it to `False`.
    """
    options = webdriver.ChromeOptions()
    if RUN_AS_HEADLESS:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=options)
    driver.set_window_size(1120, 750)
    return driver


def signin(driver):
    driver.get(SIGNIN_URL)
    random_wait(driver)

    driver.find_element_by_id("ap_email").send_keys(AMAZON_EMAIL)
    random_wait(driver)

    driver.find_element_by_id("continue").click()
    random_wait(driver)

    driver.find_element_by_id("ap_password").send_keys(AMAZON_PASSWORD)
    random_wait(driver)

    driver.find_element_by_id("signInSubmit").click()
    random_wait(driver)


def check_verification_code(driver):
    """
    Amazon may ask to send by email and input verification code
    """
    try:
        send_code_button = driver.find_element_by_id("continue")
        print("Amazon asks to send verification email")
        send_email = input("Send email? [Y/n] ") or 'Y'
        if send_email.lower() == 'y':
            send_code_button.click()
            verification_code = input("What is the verification code from email? ").strip()
            driver.find_element_by_name('code').send_keys(verification_code)
            driver.find_element_by_class_name('a-button-input').click()
            print_hr()
        else:
            print('Unable to login without verification code')
            sys.exit()
    except NoSuchElementException:
        pass


def search(driver, search_string):
    driver.find_element_by_id('twotabsearchtextbox').send_keys(search_string)
    driver.find_element_by_class_name('nav-input').click()


def print_hr():
    print('-----------')


def strip_lines(s):
    """
    Removes indents from lines in string `s`
    """
    return '\n'.join([l.strip() for l in s.split('\n')])


def format_price(s):
    """
    Combines stings in the form:

    $
    18
    04

    to

    $18.04
    """
    return re.sub(r"\$\n(\d+)\n(\d+)", '$\\1.\\2', s)


def print_product_details(html):
    """
    Prints products details found in `html` string.

    May ommit sponsored results if global flag `SKIP_SPONSORED` is set to `True`.
    Skips Shop by Category div.
    """
    soup = BeautifulSoup(html, 'html.parser')
    for element in soup.find_all(class_='s-item-container'):
        element_text = element.getText(separator=u' ').strip()
        if element_text.startswith('Sponsored'):
            if SKIP_SPONSORED:
                continue
            # clean up sponsored element text
            for e in element.find_all('h5'):
                e.extract()
            for e in element.find_all(class_='a-popover-preload'):
                e.extract()
            element_text = element.getText(separator=u' ').strip()
        if element_text.startswith('Shop by Category'):
            continue
        if element_text:
            print(
                format_price(
                    strip_lines(
                        element_text
                    )))
            print_hr()


def main():

    search_string = input('What do you want to search for? ')
    print_hr()

    driver = init_driver()
    
    signin(driver)

    check_verification_code(driver)

    search(driver, search_string)

    html = driver.page_source
    print_product_details(html)

    driver.close()


if __name__ == '__main__':
    main()
