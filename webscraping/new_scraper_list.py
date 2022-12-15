from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
options = webdriver.ChromeOptions()
# options.add_argument('user-data-dir='r'C:\Users\sathy\AppData\Local\Google\Chrome\User Data\Default')

# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get(
    "https://live.gieogita.ca/")

sign_up_btn = driver.find_element(By.XPATH, '/html/body/div/div/div[2]/div[3]/div/div[3]/div[2]/div[1]/div/div/div/div[5]/button')

sign_up_btn.click()

org_list = driver.find_element(By.XPATH, "/html/body/div/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/div[12]/div/div/div/div[2]")
org_list.click()

list_options = driver.find_elements(By.XPATH, '/html/body/div/div/div[2]/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div/div[12]/div/div/div/div[3]/ul/li')

text_options_list = []
for option in list_options:
    print(option.text)
    text_options_list.append(option.text)

with open('txt_opt.txt', 'w') as f:
    f.write(str(text_options_list))