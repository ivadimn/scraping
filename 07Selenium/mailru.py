from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time

options = Options()
options.add_argument("--disable-notifications")
options.add_argument("start-maximized")
driver = webdriver.Chrome("/home/vadim/scraping/07Selenium/chromedriver", options=options)
driver.get('https://m.mail.ru/login')
print(driver.title)
assert "Вход — Почта Mail.Ru" in driver.title


time.sleep(1)
inp = driver.find_element_by_xpath("//input[@name='Login']")
inp.send_keys('study.ai_172@mail.ru')

inp = driver.find_element_by_xpath("//input[@name='Password']")
inp.send_keys('NewPassword172')
inp.send_keys(Keys.RETURN)

def get_message_info(lnk):
    info = {}
    driver.get(lnk)
    time.sleep(2)
    theme = driver.find_element_by_xpath("//td[@class='readmsg__theme-box__line']/span")
    info["theme"] = theme.text
    msg_from = driver.find_element_by_xpath("//div[@class='readmsg__text-container']/div[1]/a")
    when = driver.find_element_by_xpath("//div[@class='readmsg__text-container']/div[2]/div/span")
    info["from"] = msg_from.text
    info["date"] = when.text
    body = driver.find_element_by_id("readmsg__body")
    info["body"] = body.text
    driver.back()
    return info

msg_list = []
while True:
    time.sleep(2)
    l_links = WebDriverWait(driver,3).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[@class='messageline__link']")))
    print(len(l_links))
    link_list = []
    for link in l_links:
        link_list.append(link.get_attribute("href"))

    for href in link_list:
        info = get_message_info(href)
        msg_list.append(info)
    try:
        a_next = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, "//a[@title='Следующая страница']")))
        driver.get(a_next.get_attribute("href"))
    except:
        break


client = MongoClient("localhost",27017)
db = client["mailru"]
db_msgs = db.messages
try:
    db_msgs.insert_many(msg_list)
except:
    print("Ошибка записи в базу")

client.close()
driver.quit()