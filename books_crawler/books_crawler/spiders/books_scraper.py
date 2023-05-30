import scrapy
from scrapy.http import Request

from books_crawler.items import BooksCrawlerItem


class BooksScrapeSpider(scrapy.Spider):
    name = "books_scrape"
    allowed_domains = ["books.toscrape.com"]
    # start_urls = ["https://books.toscrape.com/"]

    #  Scenario - Scrapy Arguments (Scrape only specific category of books)
    def __init__(self, category):
        self.start_urls = [category]

    def parse(self, response):
        #  Get urls for each book in page

        books_url = response.css("h3 a::attr(href)").extract()      #list of urls

        # print(books_url)

        for book_url in books_url:

            # print(book_url)

            #  Method 2
            # book_url = book_url.replace("../../../" , "https://books.toscrape.com/catalogue/")

            # print(response.urljoin(book_url))

            # Method 1
            yield Request(response.urljoin(book_url), callback=self.scrape_book)

        #  logic to implement navigation to Next Page
       
        try:       
            nextpage_url = response.css("li.next a::attr(href)").extract_first()

            if nextpage_url is not None: 
                yield Request(response.urljoin(nextpage_url), callback=self.parse)
        except:
            self.logger.info("----- No more pages to scrape ----- ")


    def scrape_book(self, response):
        # Logic to get data from book page
        
        items = BooksCrawlerItem() # instance of class in items.py

        book_title = response.css("div[class='col-sm-6 product_main'] h1::text").extract_first()

        book_price = response.css("div[class='col-sm-6 product_main'] p::text").extract_first()

        book_image_url = response.css("div[class='item active'] img::attr(src)").extract_first()

        absolute_book_url = book_image_url.replace("../../", "https://books.toscrape.com/")

        # yield {'book_title' : book_title , 'book_price' : book_price , 'absolute_book_url' : absolute_book_url} 

        items['book_title'] = book_title
        items['book_price'] = book_price
        items['absolute_book_url'] = absolute_book_url

        yield items