import re
import scrapy
import pandas as pd
from restuarants_data.items import RestaurantCategoryItem


class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    def __init__(self, *args, **kwargs):
        super(DeliverooSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["deliveroo.co.uk"]        
        df = pd.read_csv('selenium/deliveroodata.csv')
        self.start_urls = df['RESTUARANT LINK'].tolist()


        self.scraped_data = pd.DataFrame(columns=['RESTUARANT URL', 'CATEGORY NAME',  'FOOD ITEM', 'FOOD ITEM PRICE'])


    def parse(self, response):
        #delivery_radius_data = response.xpath('//div[2][@class="UILines-eb427a2507db75b3 ccl-2d0aeb0c9725ce8b ccl-45f32b38c5feda86"]/span[1]').get()
       # delivery_radius_match = re.search(r'([\d.]+)\s*(mile|miles)', delivery_radius_data, re.IGNORECASE)
        # delivery_radius = delivery_radius_match.group(1) if delivery_radius_match else 'N/A'
        
        category_names = response.xpath('//div[@class="Layout-acd23e46648eee23"]/h2/text()').extract()
        #print(category_names)
        
        # Extract food items and their prices for each category
        for category_name in category_names:
            food_items = response.xpath(f'//div[@class="notranslate"]/p/text()').extract()
         #   print(food_items)
            food_item_prices = response.xpath(f'//div[@class="MenuItemCard-bd0c8b7203436423 ccl-5cae55d5d78c131f"]/span/text()').extract()
          #  print(food_item_prices)
            
            # Ensure all arrays have the same length
            max_length = max(len(food_items), len(food_item_prices))
            food_items = food_items[:max_length] + [''] * (max_length - len(food_items))
            food_item_prices = food_item_prices[:max_length] + [''] * (max_length - len(food_item_prices))

            scraped_data_temp = pd.DataFrame({
                'RESTUARANT URL': [response.url] * len(food_items),
                'CATEGORY NAME': [category_name] * len(food_items),
                'FOOD ITEM': food_items,
                'FOOD ITEM PRICE': food_item_prices
            })
            self.scraped_data = pd.concat([self.scraped_data, scraped_data_temp], ignore_index=True)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)



    def closed(self, reason):
        merged_data = pd.read_csv('selenium/deliveroodata.csv')
        merged_data = pd.merge(merged_data, self.scraped_data, left_on='RESTUARANT LINK', right_on='RESTUARANT URL', how='left')
        merged_data.drop('RESTUARANT URL', axis=1, inplace=True)
        merged_data.to_csv('merged_data.csv', index=False)
