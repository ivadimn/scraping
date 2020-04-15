from pymongo import MongoClient, errors
from pprint import pprint
import hh
import superjob

sources = ["HeadHunter", "SuperJob"]
client = MongoClient("localhost", 27017)
db = client["db_vacancys"]
vacancys = db.vacancys


def to_database(vl: list):
    count_update = 0
    count_insert = 0
    for vac in vl:
        count_doc = vacancys.count_documents({"_id": vac["_id"]})  # ищем вакансию в базе
        if (count_doc > 0):  # если документ найден,
            vac_db = vacancys.find({"_id": vac["_id"]})
            if (vac_db[0]["salary_low"] != vac["salary_low"]) \
                or (vac_db[0]["salary_high"] != vac["salary_high"]) \
                or (vac_db[0]["currency"] != vac["currency"]):    # то обновим данные по зарплате отличаются
                vacancys.update_one({"_id": vac["_id"]},
                                {"$set": {"salary_low": vac["salary_low"],
                                          "salary_high": vac["salary_high"],
                                          "currency": vac["currency"]}})
                count_update += 1
        else:
            try:
                vacancys.insert_one(vac)
            except errors.DuplicateKeyError:
                print(f"Дублирование первичного ключа при добвалении вакансии {vac['name']}")
            count_insert += 1

    print(f"Добавлено {count_insert} записей, обновлено {count_update} записей")



v_list = []
while True:
    prof_name = input("Введите наименование професcии, должности (или ENTER для выхода)...: ")
    if not prof_name:
        break
    for i in range(len(sources)):
        print(f"{i + 1}. {sources[i]}")
    source = int(input("Выберите источник поиска (1, 2 ..): "))
    if source == 1:
        v_list = hh.get_vacancy_list(prof_name, 5)
    else:
        v_list = superjob.get_vacancy_list(prof_name)
    prof_name = ""
    to_database(v_list)
    pprint(v_list)


