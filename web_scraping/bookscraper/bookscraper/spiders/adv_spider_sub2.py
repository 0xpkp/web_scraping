#  here we have implemented proxy using scrapeops api



import scrapy
from bookscraper.items import bookitems
import random
import requests
from urllib.parse import urlencode


API_KEY = '657c7409-e57d-4d5d-bf50-57adf23f1749'

# to get proxy url
def get_proxy_url(url) : 
    payload = {
        'api_key' : API_KEY,
        'url' : url
    }
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    print(f'**************************url : {proxy_url} ***********************')
    return proxy_url


class AdvSpiderSpider(scrapy.Spider):
    name = "adv_spider_sub2"                   
    allowed_domains = ["books.toscrape.com", "proxy.scrapeops.io"]     #make sure to add your proxy url domain here otherwise spider will stop after one iteration
    start_urls = ["https://books.toscrape.com/"]


    # if start_requests() is defined, the scrapy will start the spider by calling this function first. this function inseted of going to 'books.toscrape.com', it will create a proxy link for that so that our first request is also made from the proxy server
    def start_requests(self):  
        yield scrapy.Request(url = get_proxy_url(self.start_urls[0]), callback=self.parse)

    def parse(self, response):
        books = response.css("article.product_pod")
        for book in books : 
            book_url = book.css("h3 a").attrib['href']
            if "catalogue/" in book_url:
                relative_url = "https://books.toscrape.com/" + book_url
            else:
                relative_url = "https://books.toscrape.com/catalogue/" + book_url

            yield scrapy.Request(url = get_proxy_url(relative_url), callback = self.parse_book_page
                                # get request sent via proxy url
                                 )    

            next_page = response.css("li.next a").attrib['href']
            if next_page is not None:
                if "catalogue/" in next_page:
                    next_page_url = "https://books.toscrape.com/" + next_page
                else:
                    next_page_url = "https://books.toscrape.com/catalogue/" + next_page

                yield response.follow(url = get_proxy_url(next_page_url), callback = self.parse
                                # get request sent via proxy url
                                      )

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
