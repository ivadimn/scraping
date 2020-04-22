# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from vacparser.items import VacparserItem


class HhunterSpider(scrapy.Spider):
    name = 'hhunter'
    allowed_domains = ['hh.ru']
    start_link = "https://spb.hh.ru"

    def __init__(self, profession: str):
        self.start_urls = [f"https://spb.hh.ru/search/vacancy?area=2&st=searchVacancy&text={profession}&showClusters=false"]

    def parse(self, response: HtmlResponse):
        next_page = response.css("a.HH-Pager-Controls-Next::attr(href)").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        vac_links = response.xpath("//a[@data-qa='vacancy-serp__vacancy-title']/@href").extract()
        for v_link in vac_links:
            yield response.follow(v_link, callback=self.vac_parse)

    def vac_parse(self, response: HtmlResponse):
        name = response.xpath("//div[@class='vacancy-title']/h1/text()").extract_first()
        link = response.url
        salary = response.xpath("//div[@class='vacancy-title']/p/span/text()").extract()
        company_link = response.xpath("//div[@class='vacancy-company-name-wrapper']"
                                      "/a[@data-qa='vacancy-company-name']/@href").extract_first()
        company_name = response.xpath("//div[@class='vacancy-company-name-wrapper']"
                                      "/a[@data-qa='vacancy-company-name']/span/text()").extract()
        yield VacparserItem(name=name, link=link, salary=salary,
                            company_link=company_link, company_name=company_name)