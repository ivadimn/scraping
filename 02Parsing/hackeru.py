from pprint import pprint
from bs4 import BeautifulSoup as bs
import requests
import time
import re
import json
import pandas as pd

main_link = ".ctf.hackeru.pro"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
headers = {"User-Agent": user_agent}

with open("brute.txt", "r" ,encoding="UTF-8") as fb:
    subs = [line.rstrip('\n') for line in fb]

#url = f"https://{main_link}"
#response = requests.get(url, headers=headers)
#print(f"{url} - {response.status_code}")


for sub in subs:
    url = f"https://{sub}{main_link}"
    try:
        response = requests.get(url, headers=headers)
        print(f"{sub} - {response.status_code}")
    except requests.exceptions.ConnectionError:
       pass
       #print(f"{url} - connection error")

    time.sleep(0.05)


""" while True:
    url = f"{main_link}"
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
print(df) """