# -*- coding:utf-8 -*-

import sys
import logging
import string
from lxml import html
from urllib import quote


class WebSpider:
    CHEMIST_WAREHOUSE = "http://www.chemistwarehouse.com.au/search?searchtext={}&searchmode=allwords"

    def __init__(self, base_url=None, coding='utf8'):
        if base_url is None:
            base_url = self.CHEMIST_WAREHOUSE
        reload(sys)
        sys.setdefaultencoding(coding)
        self.base_url = base_url

    def cookData(self, search):
        doc = html.parse(self.base_url.format(quote(search)))
        names = doc.xpath('//a[@class="product-container search-result"]/@title')
        name = map(string.strip, names)
        print name
        # pics = doc.xpath('//a[@class="product-container search-result"]/div/div/div/img[@onerror]/@src')
        # print pics
        prices = doc.xpath('//a[@class="product-container search-result"]/div/div[@class="prices"]/span[@class="Price"]/text()')
        price = map(string.strip, prices)
        print price
        saves = doc.xpath('//a[@class="product-container search-result"]/div/div[@class="prices"]/span[@class="Save"]/text()')
        save = map(string.strip, saves)
        print save

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    spider = WebSpider()
    spider.cookData("Swisse Ultiboost 500")

    # page = requests.get('http://econpy.pythonanywhere.com/ex/001.html')
    # tree = html.fromstring(page.content)
    # print tree
    # #This will create a list of buyers:
    # buyers = tree.xpath('//div[@title="buyer-name"]/text()')
    # #This will create a list of prices
    # prices = tree.xpath('//span[@class="item-price"]/text()')
    # print 'Buyers: ', buyers
    # print 'Prices: ', prices
