import random
import string
from time import sleep
import numpy as np
from nltk.corpus import names
import os
from datetime import datetime
import calendar
import argparse

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def chrome_webdriver_options_setup():
    options = webdriver.ChromeOptions()
    chrome_opts = [
        '--disable-popup-blocking', '--ignore-certificate-errors', '--no-sandbox', '--disable-dev-shm-usage', '--incognito'
    ]

    for opt in chrome_opts:
        options.add_argument(opt)

    s = Service(ChromeDriverManager().install())
    return s, options


def create_random_string(gen_type):
    if (gen_type == 'password') | (gen_type == 'username'):
        choice_list = (string.digits + string.ascii_letters)
        characters = [i for i in choice_list]
        random_chars = np.random.choice(characters, np.random.randint(8, 12))
        final_string = ''.join(random_chars)
    else:
        choice_list = (names.words('male.txt') + names.words('female.txt'))
        final_string = np.random.choice(choice_list)
    return final_string


def get_mappers():
    gender_number_map = {
        1: 'Female',
        2: 'Male',
        3: 'Rather not say'
    }

    month_number_map = dict(
        zip(np.arange(1, 13), list(calendar.month_name)[1:]))
    return gender_number_map, month_number_map


if __name__ == '__main__':
    # 1) Get phone number input from terminal
    parser = argparse.ArgumentParser()
    parser.add_argument('phone_num', type=int,
                        help='Real phone number for e-mail verification.')
    args = parser.parse_args()
    if not isinstance(args.phone_num, (np.int32, int)):
        import sys
        sys.exit("Phone number must be an integer.")

    s, options = chrome_webdriver_options_setup()
    gender_number_map, month_number_map = get_mappers()

    # 2) Open Google account creation window
    driver = webdriver.Chrome(service=s, options=options)
    site_name = 'https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    driver.get(site_name)

    driver.execute_script('''
        const button = document.getElementsByClassName('VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-dgl2Hf ksBjEc lKxP2d FliLIb uRo0Xe TrZEUc t29vte');
        button[0].click()
        const reg_link = document.getElementsByClassName('G3hhxb VfPpkd-StrnGf-rymPhb-ibnC6b');
        reg_link[0].click()
    ''')

    # 3) Fill in the account information
    first_name = create_random_string('names')
    last_name = create_random_string('names')
    user_name = create_random_string('username')
    password = create_random_string('password')

    try:
        first_name_e = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.ID, 'firstName')))
    except:
        print('Element cannot be found.')
        driver.close()
    last_name_e = driver.find_element(By.ID, 'lastName')
    user_name_e = driver.find_element(By.ID, 'username')
    pw_e = driver.find_elements(By.CLASS_NAME, 'Xb9hP')[3]
    confirm_pw_e = driver.find_elements(By.CLASS_NAME, 'Xb9hP')[4]

    first_name_e.send_keys(first_name)
    last_name_e.send_keys(last_name)
    user_name_e.send_keys(user_name)
    pw_e.find_element(By.TAG_NAME, 'input').send_keys(password)
    confirm_pw_e.find_element(By.TAG_NAME, 'input').send_keys(password)

    # 4) Confirm to next page
    confirm = driver.find_elements(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')[1]
    confirm_btn = confirm.find_element(By.TAG_NAME, 'button')
    confirm_btn.click()

    # 5) Fill in the phone number for verification
    # sleep(1)
    # try:
    #     phone_e = WebDriverWait(driver, 1000).until(
    #         EC.presence_of_element_located((By.ID, 'phoneNumberId')))
    # except:
    #     print('Element cannot be found.')
    #     driver.close()
    sleep(2)
    phone_e = driver.find_element(By.ID, 'phoneNumberId')
    # print(phone_e.get_attribute('id'))
    # print(args.phone_num)
    phone_e.send_keys(args.phone_num)

    # 6) Confirm to next page
    next_step = driver.find_element(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')
    next_step_btn = next_step.find_element(By.TAG_NAME, 'button')
    next_step_btn.click()

    # 6)  VERIFICATION STEP - MUST BE MANUALLY COMPLETED!
    response = ''
    while response.lower() != 'c':
        response = input(
            '\nAutomation paused for verification code input. Type "c" to continue: ')

    next_step = driver.find_elements(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')[1]
    next_step_btn = next_step.find_element(By.TAG_NAME, 'button')
    next_step_btn.click()

    # 6) Confirm to next page
    next_step = driver.find_element(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')
    next_step_btn = next_step.find_element(By.TAG_NAME, 'button')
    next_step_btn.click()

    # 7) Fill in the birthday & gender information
    year_input = str(np.random.choice(np.arange(1990, 2000)))
    month_num = np.random.randint(1, 13)
    day_input = str(np.random.choice(np.arange(1, 28)))
    gender_num = np.random.randint(1, 4)

    try:
        day_e = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((By.TAG_NAME, 'input')))[2]
    except:
        print('Element cannot be found.')
        driver.close()
    year_e = driver.find_elements(By.TAG_NAME, 'input')[3]
    month_options = driver.find_element(
        By.CLASS_NAME, 'UDCCJb').find_elements(By.TAG_NAME, 'option')
    gender_options = driver.find_elements(By.CLASS_NAME, 'UDCCJb')[
        1].find_elements(By.TAG_NAME, 'option')

    day_e.send_keys(day_input)
    year_e.send_keys(year_input)
    month_options[month_num].click()
    gender_options[gender_num].click()

    next_step = driver.find_element(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')
    next_step_btn = next_step.find_element(By.TAG_NAME, 'button')
    next_step_btn.click()

    # Skip all non-required steps
    try:
        skip_e = WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located((
                By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')))[-1].find_element(By.TAG_NAME, 'button')
    except:
        print('Element cannot be found.')
        driver.close()
    skip_e.click()

    next_step = driver.find_elements(
        By.CLASS_NAME, 'VfPpkd-dgl2Hf-ppHlrf-sM5MNb')[1]
    next_step_btn = next_step.find_element(By.TAG_NAME, 'button')
    next_step_btn.click()

    # 8) Close browser window
    driver.close()

    # 9) Output account credentials
    write_out = [
        f'E-mail: {user_name}@gmail.com',
        f'\nPassword: {password}',
        f'\nFirst Name: {first_name}',
        f'\nLast Name: {last_name}',
        f'\nBirth Year: {year_input}',
        f'\nBirth Month: {month_number_map[month_num]}',
        f'\nBirth Day: {day_input}',
        f'\nGender Preference: {gender_number_map[gender_num]}',
        f'\nConfirmation Phone Number: {args.phone_num}'
    ]

    out_file = os.path.join(os.getcwd(), '_'.join(
        ['account_creds', datetime.now().strftime('%Y%m%d%H%M%S') + '.txt']))
    with open(out_file, 'w') as file:
        file.writelines(write_out)
