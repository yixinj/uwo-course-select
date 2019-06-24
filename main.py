import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

# TODO: add parameters to this so that it can be uploaded to github
def script():
    """[summary]
    
    Arguments:
        path {string} -- Path to the credentials file
    """
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


for i in range(20):
    # Just in case wifi disconnects, put in try loop
    try:
        script()
        print('Finished run number:', i + 1)
    except Exception as e:
        print('Error in run number:', i + 1)
        print(e)
    # Timeout warning 1680000 ms, so I want it to refresh or smth every 1500000 ms ~roughly 25 minutes
    time.sleep(1500)