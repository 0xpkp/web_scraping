# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

class BookscraperPipeline:
    def process_item(self, item, spider):

        # processing the data
        adapter = ItemAdapter(item)
        # adapter.get('variable_name') -> to get the value of that variable
        # adapter['variable_name'] = value -> assign a value to that variable
        # NOTE : both adapter.get('variable_name') and adapter['variable_name'] returns values in tuple format . (value,). 

        # fields = adapter.field_names() -> returns all the variable names
        

        # processing functions

        # to remove white spaces from start and end of the string
        # for field in adapter.field_names():
        #     value = adapter.get(field)
        #     value = value[0].strip()
        #     adapter[field] = value

        # getting rating 
        stars_string = adapter.get('rating')
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['rating'] = 0
        elif stars_text_value == "one":
            adapter['rating'] = 1
        elif stars_text_value == "two":
            adapter['rating'] = 2
        elif stars_text_value == "three":
            adapter['rating'] = 3
        elif stars_text_value == "four":
            adapter['rating'] = 4
        elif stars_text_value == "five":
            adapter['rating'] = 5

        # getting stock value
        availability_string = adapter.get('stock')
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            adapter['stock'] = 0
        else:
            availability_array = split_string_array[1].split(' ')
            adapter['stock'] = int(availability_array[0])

        return item





















# saving the scraped values to the mysql database
import mysql.connector as conn

class mysql_connection  :
    def __init__(self) -> None:
        self.connector = conn.connect(
            host="localhost", port='3306', user='root', password='root')
        
        self.cur = self.connector.cursor()

        # creating a database
        query = 'create database if not exists bot'
        self.cur.execute(query)
        # selecting the database
        query = 'use bot'
        self.cur.execute(query)

    # creating table
        query = 'CREATE TABLE IF NOT EXISTS data(url text, name text, category text, description text default NULL, upc text, product_type text, final_price text, tax text, stock int, rating int);'

        self.cur.execute(query)
        
    def process_item(self, item, spider):

        # inserting into the table
        query = f'''insert into data(url, name, category, upc, product_type, final_price, tax, stock, rating) values('{item['url']}', "{item['name'][0]}", '{item['category'][0]}', '{item['upc'][0]}', '{item['product_type'][0]}', '{item['final_price'][0]}', '{item['tax'][0]}', {item['stock']}, {item['rating']})'''
        self.cur.execute(query)

        # commiting the changes
        self.connector.commit()
        return item

    # this function will automatically execute at the end.
    def close_spider(self, spider):
        '''  function to close the mysql database connection'''
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()