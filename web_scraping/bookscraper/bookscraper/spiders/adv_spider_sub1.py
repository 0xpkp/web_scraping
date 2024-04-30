# adv_spider + implementation of fake user agents and fake response headers from scrapeops api
# NOTE : while using fake user agents, enable only 'getuseragents' middleware and disable everything else and while using fake response headers, enable only 'getrequestheaders' middleware and disable everything else.


import scrapy
from bookscraper.items import bookitems


class AdvSpiderSpider(scrapy.Spider):
    name = "adv_spider_sub1"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com/"]

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books : 
            book_url = book.css("h3 a").attrib['href']
            if "catalogue/" in book_url:
                relative_url = "https://books.toscrape.com/" + book_url
            else:
                relative_url = "https://books.toscrape.com/catalogue/" + book_url

            yield scrapy.Request(relative_url, callback = self.parse_book_page)

            next_page = response.css("li.next a").attrib['href']
            if next_page is not None:
                if "catalogue/" in next_page:
                    next_page_url = "https://books.toscrape.com/" + next_page
                else:
                    next_page_url = "https://books.toscrape.com/catalogue/" + next_page

                yield response.follow(next_page_url, callback = self.parse)

    def parse_book_page(self, response):
        table_rows = response.css('table tr') # it will return all the rows in the table.

        book_items = bookitems() # object for 'bookitems' class


        book_items['url'] = response.url
        book_items['name'] = response.css('.product_page .product_main h1::text').get(),
        book_items['category'] = response.xpath('//ul[@class="breadcrumb"]/li[@class="active"]/preceding-sibling::li[1]/a/text()').get(),
        book_items['description'] = response.xpath('//div[@id = "product_description"]/following-sibling::p/text()').get(),
        book_items['upc'] = table_rows[0].css('td::text').get(),
        book_items['product_type'] = table_rows[1].css('td::text').get(),
        book_items['final_price'] = table_rows[3].css('td::text').get(),
        book_items['tax'] = table_rows[4].css('td::text').get(),
        book_items['stock'] = table_rows[5].css('td::text').get()
        book_items['rating'] = response.css('p.star-rating').attrib['class']
        yield book_items
