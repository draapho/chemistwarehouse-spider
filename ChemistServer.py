# -*- coding:utf-8 -*-
# pyinstaller.exe --windowed ChemistServer.py

import myutil
import logging
import time
import ChemistSpider
from tendo import singleton

LOG_FILE = myutil.get_cur_dir() + "\logging.txt"


def chemistServer():
    while True:
        logging.info("Start Chemist Spider Server...")

        # 判断什么时候需要运行, 一天只需要抓一次数据
        run = True
        date = time.strftime("%Y-%m-%d", time.localtime())
        with open(LOG_FILE) as f:
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
        logging.info("Run {}, then sleep {} hours".format("success" if run else "failed", wait))
        time.sleep(wait * 3600)


if __name__ == "__main__":
    myutil.logging_init(level=logging.INFO, file=LOG_FILE)
    me = singleton.SingleInstance()
    chemistServer()
