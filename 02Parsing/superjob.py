from pprint import pprint
from bs4 import BeautifulSoup as bs
from requests import get
import re
import json
import pandas as pd

main_link = "https://www.superjob.ru"
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
accept = "text/html,application/xhtml+xml,application/xml;q=0.9"
accept_language = "ru-RU"
accept_charset = "utf-8"
email = "ivadimn@gmail.com"
headers = {"User-Agent": user_agent, "Accept" : accept,
           "Accept-Language" : accept_language, "Accept-Charset": accept_charset,
           "From": email, "Referer": "http://ru.wikipedia.org/wiki/Main_Page"}


def parse_money(m: str, d: dict):
    m = m.replace(" ", "")
    m = m.replace("\u00a0", "")
    val = re.findall("[\D]+$", m)
    if val:
        d["currency"] = val[0]
        m = m[:-len(val[0])]
    else:
        d["currency"] = None
    m = re.sub("[^\w]+", " ", m)
    if m.startswith("от"):
        mlow = re.findall("[0-9]+", m)
        d["salary_low"] = int(mlow[0])
        d["salary_high"] = None
    elif (m.startswith("до")):
        mhigh = re.findall("[0-9]+", m)
        d["salary_high"] = int(mhigh[0])
        d["salary_low"] = None
    elif (" " in m):
        ml = m.split(" ")
        d["salary_low"] = int(ml[0])
        d["salary_high"] = int(re.findall("[0-9]+", ml[1])[0])
    else:
        if m.isdigit():
            d["salary_low"] = int(m)
            d["salary_high"] = int(m)
        else:
            d["salary_low"] = None
            d["salary_high"] = None

def save(vl : list, fname: str):
    json_data = json.dumps(vl)
    with open(fname, "w", encoding="utf-8") as fs:
        json.dump(json_data, fs)

ps = 0
prof_name = input("Введите наименование професcии, должности ...: ")
page = f"/vacancy/search/?keywords={prof_name}"
vacancy_list = []

def save_html(html_text: str):
     with open("job.html", "w", encoding="utf-8") as fs:
         fs.write(html_text)
         fs.close()

while True:
     url = f"{main_link}{page}"
     response = get(url, headers=headers)
     soup = bs(response.text, "html.parser")
     vacancy_block = soup.find("div", {"class" : "_1ID8B"})
     vacancys = vacancy_block.find_all("div", {"class": "f-test-vacancy-item"})
     for vacancy in vacancys:
         vacancy_info = {}
         a_title = vacancy.find("a", {"class": "icMQ_", "class": "_2JivQ", "class": "_1UJAN"})
         vacancy_info["name"] = a_title.getText()
         n = a_title.getText()
         vacancy_info["link"] = f"{main_link}{a_title.attrs['href']}"
         span_money = vacancy.find("span", {"class": "f-test-text-company-item-salary"})
         if span_money:
             parse_money(span_money.getText(), vacancy_info)
         else:
             vacancy_info["currency"] = None
             vacancy_info["salary_low"] = None
             vacancy_info["salary_high"] = None

         vacancy_info["employer_name"] = None
         vacancy_info["employer_link"] = None
         span_employer = vacancy.find("span", {"class": "f-test-text-vacancy-item-company-name"})
         if span_employer:
             a_employer = span_employer.find("a")
             if a_employer:
                 vacancy_info["employer_name"] = a_employer.getText()
                 vacancy_info["employer_link"] = f"{main_link}{a_employer.attrs['href']}"
         span_address = vacancy.find("span", {"class": "f-test-text-company-item-location"})
         if span_address:
             childs_span = span_address.findAll("span")
             chs = childs_span[2].find("span")
             if chs:
                 vacancy_info["employer_address"] = chs.getText()
             else:
                vacancy_info["employer_address"] = childs_span[2].getText()
         vacancy_list.append(vacancy_info)

     button_next = soup.find("a", {"class": "f-test-button-dalshe", "class": "f-test-link-Dalshe"})
     if (button_next):
         page = button_next.attrs["href"]
     else:
         break

pprint(vacancy_list)
save(vacancy_list, f"superjob_{prof_name}.json")
df = pd.DataFrame(vacancy_list)
print(df)

