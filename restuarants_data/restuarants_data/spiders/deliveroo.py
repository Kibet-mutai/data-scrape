import re
import scrapy
import pandas as pd
from restuarants_data.items import RestaurantCategoryItem


class DeliverooSpider(scrapy.Spider):
    name = "deliveroo"
    def __init__(self, *args, **kwargs):
        super(DeliverooSpider, self).__init__(*args, **kwargs)
        
        # Load restaurant links from the CSV file
        self.allowed_domains = ["deliveroo.co.uk"]
        # df = pd.read_csv('deliverooptwt.csv')
        df = pd.read_csv('selenium/deliverooptwt.csv')
        self.start_urls = df['RESTUARANT LINK'].tolist()
        # Create a DataFrame to store the scraped data
        self.scraped_data = pd.DataFrame(columns=['CATEGORY NAME', 'RESTUARANT URL', 'DELIVERY RADIUS'])



    def parse(self, response):
            # Extract the delivery radius (adjust the XPath as needed)
        delivery_radius_data = response.xpath('//div[2][@class="UILines-eb427a2507db75b3 ccl-2d0aeb0c9725ce8b ccl-45f32b38c5feda86"]/span[1]').get()

        # Use regex to extract the delivery radius (if available)
        delivery_radius_match = re.search(r'([\d.]+)\s*(mile|miles)', delivery_radius_data, re.IGNORECASE)
        delivery_radius = delivery_radius_match.group(1) if delivery_radius_match else 'N/A'
        category_names = response.xpath('//ul[@class="UILayoutGrid-99a474f58af4cb2d"]/li/a/div/div/span[contains(@class, "ccl-0956b2f88e605eb8")]/text()').extract()
        if not category_names:
            category_names = ['EMPTY']

    # for category_name in category_names:
        restuarant_url = response.url
        # print(category_name)
        scraped_data_temp = pd.DataFrame({
            'CATEGORY NAME': category_names,
            'RESTUARANT URL': [response.url] * len(category_names),
            'DELIVERY RADIUS': [delivery_radius] * len(category_names)
        })
        self.scraped_data = pd.concat([self.scraped_data, scraped_data_temp], ignore_index=True)


    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse)



    def closed(self, reason):
           # Merge the scraped data with the original data based on RESTAURANT URL
        merged_data = pd.read_csv('selenium/deliverooptwt.csv')

        # Set 'RESTUARANT LINK' as the key for merging
        merged_data = pd.merge(merged_data, self.scraped_data, left_on='RESTUARANT LINK', right_on='RESTUARANT URL', how='left')

        # Drop the duplicated column 'RESTAURANT URL'
        merged_data.drop('RESTUARANT URL', axis=1, inplace=True)

        # Save the merged data to a CSV file
        merged_data.to_csv('merged_data.csv', index=False)