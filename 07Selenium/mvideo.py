from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import json
from pymongo import MongoClient
import time


options = Options()
options.add_argument("--disable-notifications")
options.add_argument("start-maximized")
driver = webdriver.Chrome("/home/vadim/scraping/07Selenium/chromedriver", options=options)
driver.get("https://www.mvideo.ru")
hits_path = "//div[@class='gallery-layout sel-hits-block '][1]"
items_path = ".//li[@class='gallery-list-item']"
action = ActionChains(driver)
prod_list = []

driver.execute_script("window.scrollTo(0, 2500)")
time.sleep(2)
hits_block = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, hits_path)))
a_list = WebDriverWait(hits_block, 10).until(EC.presence_of_all_elements_located((By.XPATH, ".//div[@class='carousel-paging']/a")))

for a in a_list:
    time.sleep(2)
    hits_block = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, hits_path)))
    products = WebDriverWait(hits_block, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gallery-list-item")))

    for product in products:
        prod = {}
        detail = product.find_element_by_xpath(".//a[@class='sel-product-tile-title']")
        data = json.loads(detail.get_attribute("data-product-info"))
        prod["link"] = detail.get_attribute("href")
        prod["name"] = data["productName"]
        prod["_id"] = data["productId"]
        del data["productName"]
        del data["productId"]
        prod["detail"] = data
        prod_list.append(prod)

    #action.move_to_element(hits_block).perform()
    time.sleep(2)
    #a.click()               говорит что не кликабельна
    action.click(a)          # здесь кликает но товары не двигаются

    # этот вариант у меня тоже не работант
    #button = hits_block.find_element_by_xpath(".//a[contains(@class, 'sel-hits-button-next')]")
    #print(button.get_attribute("class"))
    #if "disabled" in button.get_attribute("class"):
    #    break
    #else:
    #    action.click(button)
        #button.click()

pprint(prod_list)

client = MongoClient("localhost",27017)
db = client["mvideo"]
db_hits = db.mvideo

for p in prod_list:
    if not db_hits.count_documents(p):
        db_hits.insert_one(p)
client.close()

driver.quit()


