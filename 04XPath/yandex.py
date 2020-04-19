from pprint import pprint
import requests
from lxml import html
import re
from datetime import datetime, timedelta
import db

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
main_link = "https://yandex.ru"
page = "/news/"
headers = {"User-Agent": user_agent}
list_news = []

def parse_info(info):
    time_l = re.findall("[\d]{2}:[\d]{2}$", info)
    dt = datetime.now()
    if (info.find("вчера") >= 0):
        dt = dt - timedelta(days=1)
        info = info.replace("вчера", " ")
    if (len(time_l) > 0):
        time = f"{dt.strftime('%Y-%m-%d')} {time_l[0]}:00"
        source = info[:info.find(time_l[0])].strip()
    else:
        time = f"{dt.strftime('%Y-%m-%d')} 00:00:00"
        source = info
    return time, source


def parse_news(r):
   items = r.xpath("//td[@class='stories-set__item']")
   pprint(len(items))

   for item in items:
        new = {}
        link = item.xpath(".//div[@class='story__topic']/h2/a/@href")
        if(len(link) > 0):
            full_link = link[0]
            if (not full_link.startswith("http")):
                full_link = f"{main_link}{full_link}"
            new["link"] = full_link
        else:
            new["link"] = None
        name = item.xpath(".//div[@class='story__topic']/h2/a/text()")
        if (len(name) > 0):
            new["name"] = name[0]
        else:
            new["name"] = None
        info = item.xpath(".//div[@class='story__info']/div[@class='story__date']/text()")
        new["date"], new["source"] = parse_info(info[0])
        list_news.append(new)

response = requests.get(f"{main_link}{page}", headers=headers)
print(response.status_code)
root = html.fromstring(response.text)
parse_news(root)
pprint(list_news)
db.to_database(list_news)


