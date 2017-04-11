# -*- coding:utf-8 -*-

import myutil
import logging
import ChemistSpider

if __name__ == "__main__":
    myutil.logging_init(file="local", append=True)
    try:
        spider = ChemistSpider.ChemistSpider()
        map(spider.saveProductsInfo, ChemistSpider.CATEGORIES)
    except Exception as e:
        logging.error(e)
