from pymongo import MongoClient, errors
from pprint import pprint

sources = ["HeadHunter", "SuperJob"]
client = MongoClient("localhost", 27017)
db = client["db_vacancys"]
vacancys = db.vacancys

summa = 0
print("Поиск вакансий с зарплатой большей заданной !")
while True:
    summa = int(input("Введите желаемый размер зарплаты (или 0 для выхода)...: "))
    if (summa == 0): break
    count_docs = vacancys.count_documents({"salary_high" : {"$gt" : summa}})
    if (count_docs > 0):
        val_list = vacancys.find({"salary_high" : {"$gt" : summa}})
        print("Найдены следующие вакансии: ")
        for vac in val_list:
            print(f"Профессия: {vac['prof_name']}")
            print(f"Наименование вакансии: {vac['name']}")
            print(f"Работодатель: {vac['employer_name']}, {vac['employer_link']}")
            print(f"Вилка : от {vac['salary_low']} до {vac['salary_high']} {vac['currency']}")
            print("-" * 50)
    else:
        print("Вакансий с зарплатой {summa} не найдено")
    summa = 0