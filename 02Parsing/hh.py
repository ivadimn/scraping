from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import re
import json
import pandas as pd

main_link = "https://spb.hh.ru"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
headers = {"User-Agent": user_agent}



def parse_money(m: str, d: dict):
    mold = m
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
        d["salary_low"] = None
        d["salary_high"] = None


def save(vl : list, fname: str):
    json_data = json.dumps(vl)
    with open(fname, "w", encoding="utf-8") as fs:
        json.dump(json_data, fs)


def load(fname: str) -> list:
    with open("fname", "r", encoding="utf-8") as fs:
        data = json.load(fs)
    return json.loads(data)


ps = 0
prof_name = input("Введите наименование професcии, должности ...: ")
page = f"/search/vacancy?area=2&st=searchVacancy&text={prof_name}"
vacancy_list = []

while True:
    url = f"{main_link}{page}"
    response = requests.get(url, headers=headers)
    soup = bs(response.text, "html.parser")
    vacancys = soup.find_all("div", {"data-qa": "vacancy-serp__vacancy",
                                      "class": "vacancy-serp-item"})
    print(f"Страница - {ps}")
    for vacancy in vacancys:
        vacancy_info = {}
        a_title = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-title"})
        vacancy_info["name"] = a_title.getText()
        vacancy_info["link"] = a_title.attrs["href"]
        span_money = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"})
        if span_money:
            parse_money(span_money.getText(), vacancy_info)
        else:
            vacancy_info["currency"] = None
            vacancy_info["salary_low"] = None
            vacancy_info["salary_high"] = None
        a_employer = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"})
        if a_employer:
            vacancy_info["employer_name"] = a_employer.getText()
            vacancy_info["employer_link"] = f"{main_link}{a_employer.attrs['href']}"

        else:
            # это если нет наименования работодателя
            span = vacancy.find("span", {"class": "bloko-icon_initial-action"})
            if span:
                parent = span.parent
                vacancy_info["employer_link"] = parent.attrs['href']
                vacancy_info["employer_name"] = parent.parent.getText()

        span_address = vacancy.find("span", {"data-qa":"vacancy-serp__vacancy-address"})
        if span_address.findChildren():
            vacancy_info["employer_address"] = span_address.contents[0][:-1]
        else:
            vacancy_info["employer_address"] = span_address.contents[0]

        metro = span_address.find("span", {"class": "metro-station"})

        vacancy_list.append(vacancy_info)

    ps += 1
    button = soup.find("a", {"data-qa":"pager-next"})
    #ограничимся 10 страницами (больше соединение валится)
    if(button and ps < 10):
        page = button.attrs["href"]
    else:
        break
pprint(vacancy_list)
save(vacancy_list, f"hh_{prof_name}.json")
df = pd.DataFrame(vacancy_list)
print(df)

