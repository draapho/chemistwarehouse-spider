# -*- coding:utf-8 -*-

import logging
import myutil
import MySQLdb as db


class ChemistDatabase:

    def __init__(self):
        self.connect = None

    def openDatabase(self):
        # 连接到 MySQL, 准备写入数据
        try:
            self.connect = db.connect(
                'localhost', 'root', 'root', 'chemistwarehouse')
        except Exception as e:
            logging.error(e)
            if self.connect:
                self.connect.close()
                self.connect = None

    def closeDatabase(self):
        try:
            if self.connect:
                self.connect.close()
        except Exception as e:
            logging.error(e)
        finally:
            self.connect = None

    def creatTable(self):
        self.openDatabase()
        with self.connect:
            cur = self.connect.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS products(
                         id bigint unsigned auto_increment primary key,
                         name varchar(250) not null,
                         date char(15) not null,
                         sale float not null,
                         save float not null
                         )""")
        self.closeDatabase()

    def saveDatas(self, datas, date):
        # 保存数据到 MySQL.
        with self.connect:
            cur = self.connect.cursor()
            for data in datas:
                cur.execute("INSERT INTO products(name, date, sale, save) VALUES(\'{}\', \'{}\', {}, {})".format(
                    data[0], date, data[1], data[2]))

if __name__ == "__main__":
    myutil.logging_init()
    cd = ChemistDatabase()
    # cd.openDatabase()
    # cd.closeDatabase()
    cd.creatTable()
