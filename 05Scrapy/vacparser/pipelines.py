# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re

class VacparserPipeline(object):
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.db = client.vacncys


    def process_item(self, item, spider):
        vac = {}
        if not item["name"]: return item
        if spider.name == "jobru":
            vac["name"] = " ".join(item["name"])
        else:
            vac["name"] = item["name"]
        if spider.name == "jobru":
            vac["link"] = f"{spider.start_link}{item['link']}"
        else:
            vac["link"] = item["link"]
        if spider.name == "hhunter":
            self.parse_hh_salary(item["salary"], vac)
        else:
            self.parse_jobru_salary(item["salary"], vac)

        vac["company_link"] = f"{spider.start_link}{item['company_link']}"
        vac["company_name"] = self.parse_hh_company_name(item["company_name"])
        collection = self.db[spider.name]
        collection.insert_one(vac)
        return item


    def parse_hh_salary(self, s:list, v: dict):
        min = max = curr = None
        if (len(s) <= 1):
            self.set_salary(v, min, max, curr)
            return
        s = [i for i in s if (i != " ") and (i != "\u00a0")]
        for i in range(len(s)):
            s[i] = s[i].strip().replace(" ", "").replace("\u00a0", "")
        if ("от" in s):
           min = int(s[s.index("от") + 1])
        if ("до" in s):
           max = int(s[s.index("до") + 1])
        if max == None:
            curr = s[s.index("от") + 2]
        else:
            curr = s[s.index("до") + 2]
        self.set_salary(v, min, max, curr)

    def parse_hh_company_name(self, cn: list):
            c_name = ""
            for n in cn:
                if (n != " ") and (n != "\u00a0"):
                    c_name = f"{c_name} {n}"
            return c_name

    def parse_jobru_salary(self, s:list, v: dict):
        min = max = curr = None
        if (len(s) <= 1):
            self.set_salary(v, min, max, curr)
            return
        s = [i for i in s if (i != " ") and (i != "\u00a0")]
        for i in range(len(s)):
            s[i] = s[i].strip().replace(" ", "").replace("\u00a0", "")
        if ("от" in s):
           min = int(re.findall("[0-9]+", s[1])[0])
           curr = re.findall("[\D]+", s[1])[0]
        elif ("до" in s):
            max = int(re.findall("[0-9]+", s[1])[0])
            curr = re.findall("[\D]+", s[1])[0]
        else:
            if(len(s) == 2):
                min = int(s[0])
                max = int(s[0])
            else:
                min = int(s[0])
                max = int(s[1])
            curr = s[-1]

        self.set_salary(v, min, max, curr)

    def set_salary(self, v, min, max, curr):
        v["salary_low"] = min
        v["salary_high"] = max
        v["currency"] = curr