from pymongo import MongoClient, errors

def to_database(news: list):
    client = MongoClient("localhost", 27017)
    db = client["db_news"]
    news_db = db.news
    try:
        news_db.insert_many(news)
    except errors.BulkWriteError:
        print("Ошибка записи в базу")

    client.close()
    print(f"Добавлено {len(news)} записей")
