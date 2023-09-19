import scrapy
import pandas as pd


class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    def __init__(self, *args, **kwargs):
        super(DeliverooSpider, self).__init__(*args, **kwargs)
        
        # Load restaurant links from the CSV file
        self.allowed_domains = ["deliveroo.co.uk"]
        # df = pd.read_csv('deliverooptwt.csv')
        df = pd.read_csv('selenium/deliverooptwt.csv')
        self.start_urls = df['RESTUARANT LINK'].tolist()


    def parse(self, response):
        categories = []
        for cat in response.xpath('//div[@class="ccl-6ca3cb50f8689113"]/div/span'):
            category_name = cat.xpath('//div[@class="ccl-6ca3cb50f8689113"]/div/span/text()').get()
            if category_name:
                categories.append(category_name.strip())
            print("Categories for restaurant", response.url)
            yield{
                "categories": categories
            }
        # rest_name = response.xpath('//*[@id="__next"]/div/div/div[3]/div/div/div[2]/div[2]/h1/text()').get()
        # # print(rest_name)
        # yield {'rest_name':rest_name,}


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)

