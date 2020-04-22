# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacparser.items import VacparserItem


class JobruSpider(scrapy.Spider):
    name = 'jobru'
    allowed_domains = ['superjob.ru']
    start_link = "https://www.superjob.ru"

    def __init__(self, profession: str):
        self.start_urls = [f"https://www.superjob.ru/vacancy/search/?keywords={profession}&geo%5Bt%5D%5B0%5D=4"]


    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']"
                                   "/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vac_bloks = response.xpath("//div[@class ='QiY08 LvoDO']")
        for v_block in vac_bloks:
            link = v_block.xpath(".//div[@ class ='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/@href").extract_first()
            name = v_block.xpath(".//div[@ class ='_3mfro CuJz5 PlM3e _2JVkc _3LJqf']/a/text()").extract()
            salary = v_block.xpath(".//div[@class='acdxh GPKTZ _1tH7S']/span/text()").extract()
            company_link = v_block.xpath(".//div[@class='_3P0J7 _9_FPy']//a/@href").extract_first()
            company_name = v_block.xpath(".//div[@class='_3P0J7 _9_FPy']//a/text()").extract()
            pass
            yield VacparserItem(name=name, link=link, salary=salary,
                                company_link=company_link, company_name=company_name)


