# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Compose

def check_image(value):
    if (value[:2] == "//"):
        return f"http:{value}"
    return value

def clear_values(chs):
    for key in chs.keys():
        value = chs[key]
        chs[key] = value.replace("\n", "").strip()
    return chs

class LrmItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    edu = scrapy.Field(output_processor=TakeFirst())
    images = scrapy.Field(input_processor=MapCompose(check_image))
    chs = scrapy.Field(input_processor=MapCompose(clear_values))

