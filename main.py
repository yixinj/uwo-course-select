import argparse
import time
from datetime import datetime
from statistics import mode
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# TODO: remove hardcoded ID so it can be uploaded to github
def script():
    driver = webdriver.Chrome()

    ############################ LOGIN ############################
    URL = 'https://student.uwo.ca/psp/heprdweb/?cmd=login'
    USER = 'YJIAN382'
    PASS = 'Temporary!7'

    # Visit site
    driver.get(URL)

    # Wait until site loads
    assert 'Login' in driver.title
    wait = WebDriverWait(driver, 10)

    # Tries to login
    wait.until(EC.presence_of_element_located((By.ID, 'userid')))
    driver.find_element_by_id('userid').send_keys(USER)
    driver.find_element_by_id('pwd').send_keys(PASS)
    driver.find_element_by_xpath(
        '//input[@class="PSPUSHBUTTON"][@type="Submit"]').click()

    ############################ ENROLL ############################
    ENROLL_IN_CLASSES_ID = 'WSA_SS_ACA_L0_W_WSA_ENROLL_LNK'
    PLAN_XPATH = '//a[@accesskey="P"]'
    CHECK_ID_LIST = ['P_SELECT$0']
    ENROLL_XPATH = '//input[@value="Enroll"][@type="button"][@class="PSPUSHBUTTON"]'
    FINISH_ENROLLING_XPATH = '//input[@value="Finish Enrolling"][@type="button"][@class="PSPUSHBUTTON"]'

    # Switch frame
    driver.switch_to.frame('ptifrmtgtframe')
    # Click 'Enroll in Classes' link
    # wait.until(EC.presence_of_element_located(
    #     (By.XPATH, ENROLL_IN_CLASSES_ID)))
    # driver.find_element_by_id(ENROLL_IN_CLASSES_ID).click()
    driver.execute_script(
        "submitAction_win0(document.win0,'WSA_SS_ACA_L0_W_WSA_ENROLL_LNK');")
    # Click the 'Plan' tab
    wait.until(EC.presence_of_element_located((By.XPATH, PLAN_XPATH)))
    driver.find_element_by_xpath(PLAN_XPATH).click()
    # Check checkboxes, then press 'Enroll'
    # TODO: make it parameter based (can select top x courses)
    wait.until(EC.presence_of_element_located((By.ID, CHECK_ID_LIST[0])))
    for ID in CHECK_ID_LIST:
        driver.find_element_by_id(ID).click()
    driver.find_element_by_xpath(ENROLL_XPATH).click()
    # 'Finish Enrolling'
    wait.until(
        EC.presence_of_element_located((By.XPATH, FINISH_ENROLLING_XPATH)))
    driver.find_element_by_xpath(FINISH_ENROLLING_XPATH).click()

    ############################ LOGOUT ############################
    LOGOUT_ID = 'pthdr2logout'
    driver.switch_to.default_content()

    # Logout, then quit
    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.ID, LOGOUT_ID)))
    driver.find_element_by_id(LOGOUT_ID).click()
    driver.quit()


def check_periodically(p=1500, n=20):
    # Runs indefinitely if n = 0
    i = 0
    while True:
        # Just in case wifi disconnects, put in try loop
        try:
            script()
            print('Finished run number:', i + 1)
        except Exception as e:
            print('Error in run number:', i + 1)
            print(e)
        # Timeout warning 1680000 ms, so I want it to refresh or smth every 1500000 ms ~roughly 25 minutes
        time.sleep(p)
        if n == 0:
            pass
        elif i < n:
            i += 1
        else:
            break


def check_at_time(p, n, t):
    delta = datetime.strptime(t, '%m/%d/%y,%H:%M:%S') - datetime.now()
    print("Waiting", delta.seconds, "seconds.")
    time.sleep(delta.seconds)
    check_periodically(p, n)


parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--mode",
    help=
    "1: Check for spots periodically. 2: Check for spots at a certain time (local), then check periodically.",
    type=int,
    choices=[1, 2])
parser.add_argument("-p",
                    "--period",
                    help="Period (seconds) between attempts.",
                    type=int)
parser.add_argument("-n",
                    "--number",
                    help="Number of attempts before script ends.",
                    type=int)
parser.add_argument(
    "-t",
    "--time",
    help="Time at which script starts running (24hr). Format: m/d/y,H:M:S",
    type=str)
args = parser.parse_args()
m = args.mode
p = args.period
n = args.number
t = args.time

print("Mode", m)
if m == 1:
    check_periodically(p, n)
elif m == 2:
    check_at_time(p, n, t)
else:
    print("Enter a valid mode")