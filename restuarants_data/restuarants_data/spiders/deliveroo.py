import re
import scrapy
import pandas as pd
from restuarants_data.items import RestaurantCategoryItem


class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    def __init__(self, *args, **kwargs):
        super(DeliverooSpider, self).__init__(*args, **kwargs)

        self.allowed_domains = ["deliveroo.co.uk"]        
        df = pd.read_csv('selenium/deliverooptwt.csv')
        self.start_urls = df['RESTUARANT LINK'].tolist()


        self.scraped_data = pd.DataFrame(columns=['CATEGORY NAME', 'RESTUARANT URL', 'DELIVERY RADIUS', 'CATEGORY LINK'])



    def parse(self, response):
        delivery_radius_data = response.xpath('//div[2][@class="UILines-eb427a2507db75b3 ccl-2d0aeb0c9725ce8b ccl-45f32b38c5feda86"]/span[1]').get()

        delivery_radius_match = re.search(r'([\d.]+)\s*(mile|miles)', delivery_radius_data, re.IGNORECASE)
        delivery_radius = delivery_radius_match.group(1) if delivery_radius_match else 'N/A'
        category_links = response.xpath('//a[@class="UICard-fc546e6554c9acdb undefined UICard-469f33f83128feb3 UICard-20e6f74249484648"]/@href').extract()
        # other_category_names = response.xpath('//div[@class="Layout-acd23e46648eee23"]/h2').extract()
        other_category_names = response.xpath('//div[@class="Layout-acd23e46648eee23"]/h2/text()').extract()
        category_names = response.xpath('//ul[@class="UILayoutGrid-99a474f58af4cb2d"]/li/a/div/div/span[contains(@class, "ccl-0956b2f88e605eb8")]/text()').extract()
        if not category_names:
            category_names = other_category_names

        # scraped_data = []
        for category_name in category_names:
            food_items =response.xpath('//div[@class="notranslate"]/p/text()').extract()
            food_item_prices = response.xpath('//div[@class="MenuItemCard-bd0c8b7203436423 ccl-5cae55d5d78c131f"]/span/text()').extract()
            food_name = ''
            food_price = ''

            for food_item, price in zip(food_items, food_item_prices):
                # print(f'Category: {category_name}, Food Item: {food_item}, Price: {price}')

                food_name =food_item
                print(food_name)
                food_price = food_price
            


                # Ensure all arrays have the same length
        max_length = max(len(category_names), len(category_links))
        category_names = category_names[:max_length] + [''] * (max_length - len(category_names))
        category_links = category_links[:max_length] + [''] * (max_length - len(category_links))
        # food_name = food_name[:max_length] + [''] * (max_length - len(food_name))
        # food_price = food_price[:max_length] + [''] * (max_length - len(food_price))

        scraped_data_temp = pd.DataFrame({
            'CATEGORY NAME': category_names,
            'RESTUARANT URL': [response.url] * len(category_names),
            'DELIVERY RADIUS': [delivery_radius] * len(category_names),
            'CATEGORY LINK': category_links,
            'FOOD ITEM': food_name,
            'FOOD ITEM PRICE': food_price
        })
        self.scraped_data = pd.concat([self.scraped_data, scraped_data_temp], ignore_index=True)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)



    def closed(self, reason):
        merged_data = pd.read_csv('selenium/deliverooptwt.csv')
        merged_data = pd.merge(merged_data, self.scraped_data, left_on='RESTUARANT LINK', right_on='RESTUARANT URL', how='left')
        merged_data.drop('RESTUARANT URL', axis=1, inplace=True)
        merged_data.to_csv('merged_data.csv', index=False)