import requests
import json

github_link = "http://api.github.com/users/"
what = "repos"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
headers = {"User-Agent": user_agent}

def show_repos(data: list, user: str):
    if len(data) == 0: return
    print(f"Список открытых репозиториев пользоватeя: {user}")
    for i in range(len(data)):
        print(f"Имя репозитория: {data[i]['name']}")
        print(f"\tПолное имя: {data[i]['full_name']}")
        print(f"\tURL: {data[i]['html_url']}")
        print(f"\tДата создания: {data[i]['created_at']}")
        print(f"\tПоследняя дата обновленяи: {data[i]['updated_at']}")
        print(f"\tРазмер: {data[i]['size']}")
        print("-" * 50)


def repos_to_file(data: list, user: str):
    json_file = f"{user}_repos.json"
    json_data = json.dumps(data)
    with open(json_file, "w", encoding="utf-8") as fs:
        json.dump(json_data, fs)

while True :
    user_name = input("Введите имя пользователя или нажмиете ENTER для выхода :")
    if user_name :
        response = requests.get(f"{github_link}{user_name}/{what}", headers=headers)
        if response.ok:
            data = json.loads(response.text)
            show_repos(data, user_name)
            repos_to_file(data, user_name)
        else:
            print(f"Ошибка - код ошибки: {response.status_code}")
        user_name = ""
    else:
        break
