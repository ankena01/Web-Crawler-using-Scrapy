import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class BooksSpider(CrawlSpider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    # define rules for crawling

    rules = (Rule(LinkExtractor(allow=('travel','mystery')) , follow = False , callback = 'parse'),)

    def parse(self, response):
        pass
