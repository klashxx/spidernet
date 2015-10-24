#!/usr/bin/env python

from datetime import datetime
from twisted.internet import reactor
import scrapy
import re
import locale
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from bs4 import BeautifulSoup


class LotoItem(scrapy.Item):
    date = scrapy.Field()
    winner = scrapy.Field()
    stars = scrapy.Field()

class LotoSpider(scrapy.Spider):

    name = "Loto"
    allowed_domains = ["loteriasyapuestas.es"]
    start_urls = [
        'http://www.loteriasyapuestas.es/es/buscador?type=results'
    ]

    @staticmethod
    def get_lotto_date(lotto_date):

        try:
            lotto_date = re.search(r'\d+.*$', lotto_date).group()
            try:
                lotto_date = datetime.strptime(lotto_date, '%d de %B de %Y')
            except ValueError:
                pass
        except AttributeError:
            pass

        return lotto_date      

    def parse(self, response):

        #for sel in response.xpath('//div[contains(@class, "primitiva") '
        #                          'or contains(@class, "euromi")]/div'):
  
        for sel in response.xpath('//div[contains(@class, "euromillon")]/div'):
            soup = BeautifulSoup(sel.extract(), 'html.parser')
            res = [int(num.string) for num in soup.find_all('li')]
            
            if not res:
                continue

            item = LotoItem()
            item['winner'] = res[:5]
            item['stars'] = res[5:]
            item['date'] = self.get_lotto_date(soup.h3.string)

            yield item

def main():
    locale.setlocale(locale.LC_TIME, 'es_ES')

    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    runner = CrawlerRunner()

    d = runner.crawl(LotoSpider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    return None


if __name__ == "__main__":
    main()
