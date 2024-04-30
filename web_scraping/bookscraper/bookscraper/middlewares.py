# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class BookscraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class BookscraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)



from random import randint
import requests
from urllib.parse import urlencode   

# class for getting fake user-agents
class getuseragents : 

    @classmethod
    def from_crawler(cls, crawler):
        '''function to access crawler settings'''
        return cls(crawler.settings)
    
    def __init__(self, settings) : 
        self.scrapeops_apikey = settings.get('SCRAPEOPS_APIKEY')
        self.scrapeops_useragent_endpoint = settings.get('SCRAPEOPS_USERAGENT_ENDPOINT', 'https://headers.scrapeops.io/v1/user-agents')
        self.scrapeops_useragent_active = settings.get('SCRAPEOPS_USERAGENT_ACTIVE', False)
        self.scrapeops_useragent_resultcount = settings.get('SCRAPEOPS_USERAGENT_RESULTCOUNT')

        self.scrapeops_useragents_list = []
        self.get_useragent_list()
        self.scrapeops_useragent_enabled()

    def get_useragent_list(self):
        payload = {'api_key' : self.scrapeops_apikey}
        if self.scrapeops_useragent_resultcount is not None : 
            payload['num_results'] = self.scrapeops_useragent_resultcount

        response = requests.get(self.scrapeops_useragent_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.scrapeops_useragents_list = json_response.get('result', [])

    def get_random_useragent(self) :
        random_index = randint(0, len(self.scrapeops_useragents_list)-1)
        return self.scrapeops_useragents_list[random_index]
    
    def scrapeops_useragent_enabled(self) :
        if self.scrapeops_apikey is None or self.scrapeops_apikey == '' or self.scrapeops_useragent_active == False : 
            self.scrapeops_useragent_active = False
        else : 
            self.scrapeops_useragent_active = True

    # scrapy will automatically execute this function
    def process_request(self, request, spider) :
        random_useragent = self.get_random_useragent()
        request.headers['User-Agent'] = random_useragent   #setting the user-agent

        # for verification
        print("*****************new user-agent*****************")
        print(request.headers['User-Agent'])

# class for getting fake request headers
class getrequestheaders : 

    @classmethod
    def from_crawler(cls, crawler):
        '''function to access crawler settings'''
        return cls(crawler.settings)
    
    def __init__(self, settings) : 
        self.scrapeops_apikey = settings.get('SCRAPEOPS_APIKEY')
        self.scrapeops_header_endpoint = settings.get('SCRAPEOPS_HEADER_ENDPOINT')
        self.scrapeops_header_active = settings.get('SCRAPEOPS_HEADER_ACTIVE')
        self.scrapeops_header_resultcount = settings.get('SCRAPEOPS_HEADER_RESULTCOUNT')

        self.scrapeops_headers_list = []
        self.get_headers_list()
        self.scrapeops_headers_enabled()

    def get_headers_list(self):
        payload = {'api_key' : self.scrapeops_apikey}
        if self.scrapeops_header_resultcount is not None : 
            payload['num_results'] = self.scrapeops_header_resultcount
        response = requests.get(self.scrapeops_header_endpoint, params=urlencode(payload))
        json_response = response.json()
        self.scrapeops_headers_list = json_response.get('result', [])
    
    def scrapeops_headers_enabled(self):
        if self.scrapeops_apikey is None or self.scrapeops_apikey == '' or self.scrapeops_header_active == False:
            self.scrapeops_header_active = False
        else : 
            self.scrapeops_header_active = True
    
    def get_random_header(self) : 
        random_index = randint(0, len(self.scrapeops_headers_list)-1)
        return self.scrapeops_headers_list[random_index]

    # scrapy will automatically execute this function
    def process_request(self, request, spider) : 
        random_header = self.get_random_header()
        # request.headers = random_header   #setting the browser header
        request.headers['accept-language'] = random_header['accept-language']
        request.headers['sec-fetch-user'] = random_header['sec-fetch-user']
        request.headers['sec-fetch-mod'] = random_header['sec-fetch-mod']
        request.headers['sec-fetch-site'] = random_header['sec-fetch-site']
        request.headers['sec-ch-ua-platform'] = random_header['sec-ch-ua-platform']
        request.headers['sec-ch-ua-mobile'] = random_header['sec-ch-ua-mobile']
        request.headers['sec-ch-ua'] = random_header['sec-ch-ua']
        request.headers['accept'] = random_header['accept']
        request.headers['user-agent'] = random_header['user-agent']
        request.headers['upgrade-insecure-requests'] = random_header['upgrade-insecure-requests']

        # for verification
        print("*****************new header*****************")
        print(request.headers)

