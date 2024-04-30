## adv_spider + implementation of fake user agents

import scrapy
from bookscraper.items import bookitems
import random

# list of fake user agents
user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
]

class AdvSpiderSpider(scrapy.Spider):
    name = "adv_spider_sub0"
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

            yield scrapy.Request(relative_url, callback = self.parse_book_page, 
                                 headers={'User-Agent' : user_agent_list[random.randint(0, len(user_agent_list)-1)]}
                                 )    #specifying the user agent

            next_page = response.css("li.next a").attrib['href']
            if next_page is not None:
                if "catalogue/" in next_page:
                    next_page_url = "https://books.toscrape.com/" + next_page
                else:
                    next_page_url = "https://books.toscrape.com/catalogue/" + next_page

                yield response.follow(next_page_url, callback = self.parse,
                                      headers={'User-Agent' : user_agent_list[random.randint(0, len(user_agent_list)-1)]}
                                      )   #specify user agent wherever you are making requests

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
