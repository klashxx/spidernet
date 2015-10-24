# -*- coding: utf-8 -*-

# Items are containers they work like simple Python dicts. 

import scrapy

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()