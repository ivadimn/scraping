""" Eventful - это крупнейшая в мире коллекция мероприятий,
проводимых на местных рынках по всему миру, от концертов
и спортивных игр до одиночных мероприятий
и политических митингов."""

import requests
import json

def get_category_list(url: str):
    response = requests.get(url_category)
    categories = json.loads(response.text)
    cats = categories["category"]
    names = []
    for i in range(len(cats)):
        names.append(cats[i]["name"])
    return names


app_key="Nhb4tMm7FPGWkdRX"
eventful_url = "http://api.eventful.com/json/"
url_category = "http://api.eventful.com/json/categories/list?app_key=Nhb4tMm7FPGWkdRX"

url = "http://api.eventful.com/rest//search?app_key=Nhb4tMm7FPGWkdRX&keywords=films&location=San+Diego&date=Future"
kinds = {"События": "events/search?", "Места": "venues/search?",
            "Исполнители": "performes/search?", "Требования": "demands/search?"}

print("Поиск событий, мест, известных людей, требований")
print("-" * 40)
print("Список доступных категорий для поиска")
categories = get_category_list(url_category)
print(categories)

print("-" * 40)
print("Что можно искать ....")
ks = list(kinds.keys())
for i in range(len(ks)):
    print(f"{i + 1}. {ks[i]}")

print("-" * 40)
ws = int(input("Что будем искать? (1, 2, 3, 4): "))
cat = input("Введите категорию из показанных выше: ")
place = input("Введите место: ")
url = f"{eventful_url}{kinds[ks[ws-1]]}app_key={app_key}&keywords={cat}&l={place}"

resp = requests.get(url)
result = json.loads(resp.text)
print(json.dumps(result, indent=4, sort_keys=True))

