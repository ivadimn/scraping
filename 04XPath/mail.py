from pprint import pprint
import requests
from lxml import html
import time
import db

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36"
main_link = 'https://news.mail.ru'
headers = {"User-Agent": user_agent}
list_news = []


def get_detail(href):
    source = None
    when = None
    resp = requests.get(href, headers=headers)
    r = html.fromstring(resp.text)
    s = r.xpath("//div[contains(@class, 'breadcrumbs')]//span[@class='link__text']/text()")
    if len(s) > 0:
        source = s[0]
    w = r.xpath("//div[contains(@class, 'breadcrumbs')]//span[@class='note__text breadcrumbs__text js-ago']/@datetime" \
                " | //div[contains(@class, 'breadcrumbs')]//time[@class='note__text breadcrumbs__text js-ago js-ago-wrapper']/@datetime")
    if len(w) > 0:
        when = w[0]
    return when, source


def parse_top_block(r):
      items = r.xpath("//div[contains(@class, 'daynews__item')]")
      for item in items:
          new = {}
          link = item.xpath(".//a/@href")
          if (not link[0].startswith("http")):
              full_link = f"{main_link}{link[0]}"
          else:
              full_link = link[0]
          name = item.xpath(".//span[contains(@class, 'photo__title')]/text()")
          new["link"] = full_link
          new["name"] = name[0]
          if (full_link.find("mail.ru") >= 0):
              time.sleep(0.1)
              new["date"], new["source"] = get_detail(full_link)
          list_news.append(new)


def parse_track_block(r):
    items = r.xpath("//li[contains(@class, 'list__item')]")
    for item in items:
        new = {}
        link = item.xpath(".//a/@href")
        if ((len(link) > 0) and (not link[0].startswith("http"))):
            full_link = f"{main_link}{link[0]}"
        else:
            full_link = link[0]
        name = item.xpath(".//a[@class='list__text']/text() | .//a/span/text()")
        new["link"] = full_link
        new["name"] = name[0]
        if (full_link.find("mail.ru") >= 0):
            time.sleep(0.1)
            new["date"], new["source"] = get_detail(full_link)
        list_news.append(new)



response = requests.get(main_link, headers=headers)
print(response.status_code)
root = html.fromstring(response.text)
parse_top_block(root)
parse_track_block(root)
pprint(list_news)
db.to_database(list_news)
