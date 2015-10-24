# -*- coding: utf-8 -*-


import scrapy

from spidernet.items import NewsItem

class NewsSpider(scrapy.Spider):
    """Spiders are classes that you define and Scrapy uses to scrape
    information from a domain (or group of domains)
    """
    name = "news"
    allowed_domains = ["elpais.es"]
    start_urls = [
        "http://elpais.com/lomasvisto/"
    ]

    def parse(self, response):

        # shell: for i in response.xpath('//h2/a[@href]/text()').extract():
        for sel in response.xpath('//h2'):
            item = NewsItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()

            yield item




