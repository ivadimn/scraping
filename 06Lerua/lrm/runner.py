from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from lrm import settings
from lrm.spiders.leruam import LeruamSpider

if __name__ == "__main__" :
    crw_settings = Settings()
    crw_settings.setmodule(settings)
    process = CrawlerProcess(settings=crw_settings)
    product = input("Введите наименование товара: ")
    process.crawl(LeruamSpider, product=product)
    process.start()