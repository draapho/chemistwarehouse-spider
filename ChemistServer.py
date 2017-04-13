# -*- coding:utf-8 -*-
# pyinstaller.exe --onefile ChemistServer.py

import myutil
import logging
import time
import ChemistSpider
from tendo import singleton

myutil.logging_init()
me = singleton.SingleInstance()

while True:
    with open(ChemistSpider.LOG_FILE, 'a') as f:
        f.write(time.strftime("%Y-%m-%d %H:%M:%S",
                              time.localtime()) + ": Chemist Server start ...\r")

    # 判断什么时候需要运行, 一天只需要抓一次数据
    run = True
    date = time.strftime("%Y-%m-%d", time.localtime())
    with open(ChemistSpider.LOG_FILE) as f:
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
