from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from vacparser import settings
from vacparser.spiders.hhunter import HhunterSpider
from vacparser.spiders.jobru import JobruSpider

if __name__ == "__main__" :
    crw_settings = Settings()
    crw_settings.setmodule(settings)
    process = CrawlerProcess(settings=crw_settings)
    process.crawl(HhunterSpider, profession="Python")
    #process.crawl(JobruSpider, profession="C")
    process.start()
