from scrapy_selenium import SeleniumRequest
import scrapy

class CBCSpider(scrapy.Spider):
    name = "cbc"
    
    def start_requests(self):
        url = "https://kicd.ac.ke/"
        yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response):
        subjects = response.css(".curriculum-list a::text").getall()
        yield {"subjects": subjects}
