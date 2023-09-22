import scrapy
import pandas as pd


class DeliveroofooditemsSpider(scrapy.Spider):
    name = "FoodItems"
   
    def __init__(self, *args, **kwargs):
        super(DeliveroofooditemsSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["deliveroo.co.uk"]        
        df = pd.read_csv('merged_data.csv')
        self.start_urls = df['CATEGORY LINK'].tolist()
        self.data = pd.DataFrame(['CATEGORY NAME', 'FOOD ITEM', 'ITEM PRICE', 'RESPONSE URL'])  

    def parse(self, response):
        all_elements = response.xpath('//div[@class="MenuItemCard-a927b3314fc88b17 MenuItemCard-1c229a9ab5bb702f"]')
        food_items = response.xpath('//div[@class="notranslate"]/p/span/text()').extract()
        item_price = response.xpath('//div[@class="MenuItemCard-ffce2437ec17693c"]/div/span/text()').extract()
    
        scraped_data =  {
            'FOOD ITEM' : food_items,
            'ITEM PRICE': item_price,
            'RESPONSE URL': response.url,
            'CATEGORY NAME': 'CATEGORY'
        }
        self.data = pd.DataFrame(scraped_data)
        # yield df


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)


    def closed(self, reason):
        self.data.to_csv('food-items-trial.csv', index=False)
