# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from lrm.items import LrmItem
from scrapy.loader import ItemLoader


class LeruamSpider(scrapy.Spider):
    name = 'leruam'
    allowed_domains = ['leroymerlin.ru']
    def __init__(self, product: str):
        self.start_urls = [f"https://leroymerlin.ru/search/?q={product}&suggest=true"]

    def parse(self, response):
        next_page = response.xpath("//div[@class='next-paginator-button-wrapper']/a/@href").extract_first()

        prod_links = response.xpath("//div[@class='product-name']/a/@href").extract()
        for p_link in prod_links:
            yield response.follow(p_link, callback=self.prod_parse)

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def prod_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LrmItem(), response=response)
        loader.add_xpath("name", "//h1[@itemprop='name']/text()")
        loader.add_xpath("price", "//span[@slot='price']/text()")
        loader.add_xpath("edu", "//span[@slot='unit']/text()")
        loader.add_xpath("images", "//picture[@slot='pictures']/source[1]/@srcset")
        ch_list = response.xpath("//div[@class='def-list__group']")
        ch_dict = {}
        #обработчик характеристики товара
        for ch in ch_list:
            ch_name = ch.xpath("./dt/text()").extract_first()
            ch_value = ch.xpath("./dd/text()").extract_first()
            ch_dict[ch_name] = ch_value
        loader.add_value("chs", ch_dict)
        yield loader.load_item()
        #name = response.xpath("//h1[@itemprop='name']/text()").extract_first()
        #price = response.xpath("//span[@slot='price']/text()").extract_first()
        #edu = response.xpath("//span[@slot='unit']/text()").extract_first()

        #images = response.xpath("//picture[@slot='pictures']/source[1]/@srcset").extract()

        #yield LrmItem(name=name, price=price, edu=edu, chs=ch_dict, images=images)