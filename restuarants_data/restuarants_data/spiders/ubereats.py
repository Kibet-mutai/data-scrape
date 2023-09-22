import scrapy


class UbereatsSpider(scrapy.Spider):
    name = "ubereats"
    allowed_domains = ["ubereats.com"]
    start_urls = ["https://ubereats.com"]

    def parse(self, response):
        pass
