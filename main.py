# -*- coding:utf-8 -*-

import myutil
import logging
import myutil
import time
import ChemistSpider
from tendo import singleton

if __name__ == "__main__":
    _log_file = myutil.get_cur_dir() + "\logging.txt"

    myutil.logging_init(level=logging.INFO, file=_log_file, append=True)
    me = singleton.SingleInstance()

    while True:
        # 判断什么时候需要运行, 一天只需要抓一次数据
        run = True
        date = time.strftime("%Y-%m-%d", time.localtime())
        with open(_log_file) as f:
            for line in f:
                if "products from" in line and date in line[50:]:
                    run = False
                    break

        if run:
            try:
                spider = ChemistSpider.ChemistSpider()
                map(spider.saveProductsInfo, ChemistSpider.CATEGORIES)
            except Exception as e:
                logging.error(e)

        # work again at 8 clock next day
        wait = 24 + 8 - time.localtime().tm_hour
        logging.info("Try to run: {}, then sleep {} hours".format(run, wait))
        time.sleep(wait * 3600)
