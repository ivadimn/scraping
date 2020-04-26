import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
from urllib.parse import urlparse
import re

prod_list = []
class LrmPipeline(object):
    def __init__(self):
        client = MongoClient("localhost", 27017)
        self.db = client.lrm

    def process_item(self, item, spider):
        prod = {}
        prod["name"] = item["name"]
        prod["price"] = float(item["price"])
        prod["edu"] = item["edu"]
        prod["chs"] = item["chs"]
        prod["images"] = item["images"]
        collection = self.db[spider.name]
        collection.insert_one(prod)
        return item

class LrmPhotosPipeline(ImagesPipeline):
    name: str = ""
    def get_media_requests(self, item, info):
        if item["images"]:
            self.name = item["name"]
            for img in item["images"]:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results[0][0]:
            item["images"] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        f_path = f"{self.name}/{os.path.basename(urlparse(request.url).path)}"
        return f_path