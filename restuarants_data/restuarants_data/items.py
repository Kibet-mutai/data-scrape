# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RestuarantsDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class RestaurantCategoryItem(scrapy.Item):
    # delivery_radius = scrapy.Field()
    category_name = scrapy.Field()
    # links = scrapy.Field()