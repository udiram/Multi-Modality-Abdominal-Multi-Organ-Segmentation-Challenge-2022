from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
options = webdriver.ChromeOptions()
from concurrent.futures import ThreadPoolExecutor
import threading

chrome_options.add_argument("--headless")
url = "https://github.com/udiram"
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
# driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)
def traffic():
    driver.refresh()

for i in tqdm(range(100)):
    traffic()