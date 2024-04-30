# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# variables for holding scraped data.

# sample
class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# serializer - for processing the data scraped.
def price_serializer(value):
    return f"$ {str(value)}"
# NOTE : use this method only if in small projects if you feel that you don't want to do much preprocessing. otherwise it's recommended to use pipelines.

class bookitems(scrapy.Item):
    # note : the values you yield in adv_spider.py should have same name as the 
    url =  scrapy.Field()
    name=  scrapy.Field()
    category=  scrapy.Field()
    description =  scrapy.Field()
    upc=  scrapy.Field()
    product_type=  scrapy.Field()
    # to use serializer, pass the serializer funtion to serializer
    # for example, 
        # final_price = scrapy.Field(serializer = price_serializer)  
    final_price=  scrapy.Field()
    tax =  scrapy.Field()
    stock=  scrapy.Field()
    rating = scrapy.Field()