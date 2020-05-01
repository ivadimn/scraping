from pprint import pprint
import requests
from lxml import html, etree
import time
import json


user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
main_link = 'https://www.mvideo.ru/'
headers = {"User-Agent": user_agent}
list_news = []

response = requests.get(main_link, headers=headers)
print(response.status_code)
root = html.fromstring(response.text)
#la =root.xpath("//div[@class='gallery-layout sel-hits-block ']//a[@class='next-btn sel-hits-button-next']")
#la = root.xpath("//div[@data-init='gtm-push-products']//div[contains(text(), 'Хиты продаж' )]")
la = root.xpath("//div[@class='gallery-layout sel-hits-block '][1]")
#li = la[0].xpath("./div[@class='gallery-layout sel-hits-block ']//li[@class='gallery-list-item']"
#                      "//a/@data-product-info")
lis = la[0].xpath(".//li[@class='gallery-list-item']//a[@class='sel-product-tile-title']/@data-product-info")
buttons = la[0].xpath(".//div[@class='accessories-carousel-wrapper']"
                                                       "/a[contains(@class, 'sel-hits-button-next')]")
print(buttons)
for b in buttons:
    print(b.attrib)

print(len(lis))
for li in lis:
    js = json.loads(li)
    pprint(js)



