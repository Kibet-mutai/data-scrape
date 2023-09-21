import scrapy
import pandas as pd


class DeliveroofooditemsSpider(scrapy.Spider):
    name = "FoodItems"
    allowed_domains = ["deliveroo.co.uk"]
    start_urls = [
                    "https://deliveroo.co.uk/menu/Kettering/brambleside/central-england-co-op-kettering-hallwood-road/?day=today&geohash=gcr6pmnt52wh&time=ASAP&linked_request_uuid=aac2c088-4c6b-4fff-9d24-b3083ecde256&category_id=155090856",
                    "https://deliveroo.co.uk/menu/Kettering/brambleside/central-england-co-op-kettering-hallwood-road/?day=today&geohash=gcr6pmnt52wh&time=ASAP&category_id=204450213&linked_request_uuid=b10441e6-7f49-464d-b2d0-6c8622209834"
                  ]

    def parse(self, response):
        all_elements = response.xpath('//div[@class="MenuItemCard-a927b3314fc88b17 MenuItemCard-1c229a9ab5bb702f"]')
        food_items = response.xpath('//div[@class="notranslate"]/p/span/text()').extract()
        item_price = response.xpath('//div[@class="MenuItemCard-ffce2437ec17693c"]/div/span/text()').extract()
    
        scraped_data =  {
            'FOOD ITEM' : food_items,
            'ITEM PRICE': item_price
        }
        self.df = pd.DataFrame(scraped_data)
        # yield df


    def closed(self, reason):
        self.df.to_csv('food-items.csv', index=False)

        # pass
