import scrapy


class DeliveroofooditemsSpider(scrapy.Spider):
    name = "DeliverooFoodItems"
    allowed_domains = ["deliveroo.co.uk"]
    start_urls = ["https://deliveroo.co.uk"]

    def parse(self, response):
        pass
