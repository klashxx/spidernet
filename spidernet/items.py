# -*- coding: utf-8 -*-

import scrapy

class NewsItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()