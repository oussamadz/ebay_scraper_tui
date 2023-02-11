# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EbayItem(scrapy.Item):
    # define the fields for your item here like:
    task = scrapy.Field()
    title = scrapy.Field()
    prodId = scrapy.Field()
    condition = scrapy.Field()
    price = scrapy.Field()
    sell = scrapy.Field()
    shipping = scrapy.Field()
    url = scrapy.Field()
    pass
