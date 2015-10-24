from twisted.internet import reactor
import scrapy
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
            item['date'] = soup.h3.string

            yield item

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(LotoSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run()
