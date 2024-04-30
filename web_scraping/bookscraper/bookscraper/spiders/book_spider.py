##### this spider does basic crawling and extracts basic information

import scrapy
#pip install scrapy


class BookSpiderSpider(scrapy.Spider):
    name = "book_spider"  #name of the spider
    allowed_domains = ["books.toscrape.com"]  #restricts the spider to crawl to other websites becuase webpages mostly link to other pages so we dont want our spider to follow that link and scrape all the internet.
    start_urls = ["https://books.toscrape.com"] 

    def parse(self, response):
        '''function to parse the response from the spider'''
        books = response.css('article.product_pod')     # extracting all the <article class = 'product_pod'> tags.
        for book in books:
            yield{
                'name' : book.css('h3 a').attrib['title'],  # inside the article tag we extracted, there are several other tags. from that we extract <h3> tag and then we extract <a> that is present inside the <h3> tag. then we take 'title' attribute of the <a> tag
                'price' : book.css('div.product_price p.price_color::text').get(), #here we get content of the tag
                'link' : book.css('h3 a').attrib['href']
            }
        # the webpage contains 1000 book entries but only 20 is shown in a page. you can notice 'next' button at the bottom of every page except last page.
        next_page = response.css('li.next a').attrib['href'] #here we are extracting the link for next page
        if next_page is not None: #logic for next page. if 'next page' is none, that mean we have reached the final page and it becomes false

            # some of the next page links are 'catalogue/page-1.html' where as some links are like '/page-4.html'. we handle the inconsistency below 
            if 'catalogue/' in next_page:
                next_page_link = "https://books.toscrape.com/" + next_page
            else:
                next_page_link = "https://books.toscrape.com/catalogue/" + next_page
            
            # then, we load the next page link and call this functino again.
            yield response.follow(next_page_link, callback = self.parse)
