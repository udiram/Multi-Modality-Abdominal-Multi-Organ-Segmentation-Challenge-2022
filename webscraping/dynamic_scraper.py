import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import schedule
import time

frequency = 30  # minutes


def status_check():
    chrome_options = Options()
    # chrome_options.add_experimental_option("detach", True)
    # options = webdriver.ChromeOptions()
    # options.add_argument('user-data-dir='r'C:\Users\sathy\AppData\Local\Google\Chrome\User Data\Default')

    # chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(ChromeDriverManager().install())
    # driver = webdriver.Chrome(ChromeDriverManager().install())

    driver.get(
        "https://jetstream2.exosphere.app/exosphere/projects/4fd8ae5822b0492494453cf591412a30/regions/IU/servers/2491d4c3-8bbe-4ec9-8179-8f472cc95db4")

    xsede1 = driver.find_element("xpath",
                                 "/html/body/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div/div/div/div[2]/div")
    xsede1.click()

    continue_btn = driver.find_element('xpath', '/html/body/main/div/form/button')
    continue_btn.click()

    username = driver.find_element('id', 'username')
    username.send_keys('ramu9703')

    password = driver.find_element('id', 'password')
    password.send_keys('Udi97034122!')

    login_btn = driver.find_element('xpath', '/html/body/div/div/div/div[1]/form/div[4]/button')
    login_btn.click()

    driver.switch_to.frame('duo_iframe')

    send_push = driver.find_element('xpath', '/html/body/div/div/div[1]/div/form/div[1]/fieldset/div[1]/button')
    send_push.click()

    driver.switch_to.default_content()
    driver.switch_to.parent_frame()

    # wait until page loads
    WebDriverWait(driver, 25).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[2]/div/div[2]/div/label')))
    instance = driver.find_element('xpath', '/html/body/div/div[3]/div[2]/div/div[2]/div/label')
    instance.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[2]/div/div[2]/div/label')))
    choose_btn = driver.find_element('xpath', '/html/body/div/div[3]/div[2]/div/div[2]/div/div/div')
    choose_btn.click()

    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div[3]/div[2]/div/div[2]/div/div/div/a[1]')))
    allocation = driver.find_element('xpath', '/html/body/div/div[3]/div[2]/div/div[2]/div/div/div/a[1]')
    allocation.click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[3]/div[2]/div/div[2]/div/div[3]/div/a[1]/div/div')))
    allocation2 = driver.find_element('xpath', '/html/body/div/div[3]/div[2]/div/div[2]/div/div[3]/div/a[1]/div/div')
    allocation2.click()

    WebDriverWait(driver, 15).until(EC.presence_of_element_located(
        (By.XPATH, '/html/body/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/a/div/div')))
    multi_modal = driver.find_element('xpath',
                                      '/html/body/div/div[3]/div[2]/div/div[2]/div/div/div[2]/div[2]/div/div[1]/a/div/div')
    multi_modal.click()

    driver.save_screenshot('screenshot.png')
    driver.close()
    driver.quit()
    img = cv2.imread('screenshot.png')
    top, bottom = 500, 1000
    left, right = 0, 750
    im_crop = img[top:bottom, left:right]
    cv2.imwrite('screenshot_crop.png', im_crop)

    # get top half on imcrop

    activity_crop = im_crop[100:250, 0:750]
    cv2.imwrite('activity_crop.png', activity_crop)

    # find yellow in activity_crop
    yellow = cv2.inRange(activity_crop, (0, 0, 0), (8, 179, 234))
    cv2.imwrite('yellow.png', yellow)

    im_np = np.array(yellow)
    n_white_pix = np.sum(im_np == 255)
    print(n_white_pix)
    if n_white_pix > 15:

        # create one channel black image (grayscale)
        img_black = np.zeros((3840, 2160))

        # convert to 3 channel black (color)
        img_3channel = cv2.merge([img_black, img_black, img_black])

        # draw on it in color
        cv2.rectangle(img_3channel, (0, 0), (3840, 2160), (0, 255, 0), -1)
        cv2.putText(img_3channel, 'All Systems OK', (500, 750), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 2)
        cv2.imshow('image', img_3channel)
        cv2.waitKey((frequency-1)*60000)
        cv2.destroyAllWindows()

    elif n_white_pix == 0 :

        # create one channel black image (grayscale)
        img_black = np.zeros((3840, 2160))

        # convert to 3 channel black (color)
        img_3channel = cv2.merge([img_black, img_black, img_black])

        # draw on it in color
        cv2.rectangle(img_3channel, (0, 0), (3840, 2160), (0, 0, 255), -1)
        cv2.putText(img_3channel, 'Systems Offline', (500, 750), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 0, 0), 2)
        cv2.imshow('image', img_3channel)
        cv2.waitKey((frequency-1)*60000)
        cv2.destroyAllWindows()

status_check()
schedule.every(frequency).minutes.do(status_check)

while True:
    schedule.run_pending()
    time.sleep(1)
