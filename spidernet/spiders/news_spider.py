# -*- coding: utf-8 -*-

import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    allowed_domains = ["elpais.es"]
    start_urls = [
        "http://www.elpais.es/"
    ]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)