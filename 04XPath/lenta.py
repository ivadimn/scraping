from pprint import pprint
import requests
from lxml import html
import re
from datetime import datetime
import db

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
main_link = "https://lenta.ru"
page = "/news/"
headers = {"User-Agent": user_agent}
list_news = []
months = {"января": "01", "февраля": "02", "марта": "03", "апреля": "04", "мая": "05", "июня": "06", "июля": "07",
          "августа": "08" , "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"}

def parse_date(dt, tm):
    d = re.findall("[\d]+", dt)
    m =  re.findall("[а-я]+", dt)
    if len(d) == 2:
        return f"{d[1]}-{months[m[0]]}-{d[0]} {tm}:00"
    elif len(d) == 1:
        return f"2020-{months[m[0]]}-{d[0]} {tm}:00"
    else:
        return f"{datetime.now().strftime('%Y-%m-%d')} {tm}:00"

def parse_items_article(r):
    items = r.xpath("//div[@class='item article'] | //div[@class='item news b-tabloid__topic_news']")
    for item in items:
        new = {}
        new["source"] = "Lenta.ru"
        link = item.xpath("./div[@class='titles']/h3/a/@href")
        if (len(link) > 0):
            full_link = link[0]
            if (not full_link.startswith("http")):
                full_link = f"{main_link}{full_link}"
            new["link"] = full_link
        else:
            new["link"] = None
        name = item.xpath("./div[@class='titles']/h3/a/span/text()")
        if (len(name) > 0):
            new["name"] = name[0]
        else:
            new["name"] = None
        dt = item.xpath("./div[@class='info g-date item__info']/span[@class='g-date item__date']/text()")
        tm = item.xpath("./div[@class='info g-date item__info']/span[@class='g-date item__date']/span[@class='time']/text()")
        if (len(dt) > 0 and len(tm) > 0):
            new["date"] = parse_date(dt[0], tm[0])
        else:
            new["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        list_news.append(new)


def parse_items(r):
    items = r.xpath("//div[@class='item']")
    for item in items:
        new = {}
        link = item.xpath("./a/@href")
        if (len(link) > 0):
            full_link = link[0]
            if (not full_link.startswith(main_link)):
                full_link = f"{main_link}{full_link}"
            new["link"] = full_link
        else:
            new["link"] = None
        name = item.xpath("./a/text()")
        if (len(name) > 0):
            new["name"] = name[0]
        else:
            new["name"] = None
        new["source"] = "Lenta.ru"
        dt = item.xpath("./a/time[@class='g-time']/@title")
        tm = item.xpath("./a/time[@class='g-time']/text()")
        if (len(dt) > 0 and len(tm) > 0):
            new["date"] = parse_date(dt[0], tm[0])
        else:
            new["date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        list_news.append(new)

response = requests.get(f"{main_link}{page}", headers=headers)
print(response.status_code)
root = html.fromstring(response.text)
parse_items(root)
parse_items_article(root)
print(len(list_news))
pprint(list_news)
db.to_database(list_news)


