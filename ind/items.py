# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IndItem(scrapy.Item):
    Date = scrapy.Field()
    Price = scrapy.Field()
    UniqueId = scrapy.Field()
    Region = scrapy.Field()
    CommodityID = scrapy.Field()
