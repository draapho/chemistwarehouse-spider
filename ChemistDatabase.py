# -*- coding:utf-8 -*-

import logging
import myutil
import itertools
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

    def searchName(self, key):
        # 搜索产品名称， 根据空格分解为多个关键字查询
        keys = myutil.trim_str(key).split()
        cmd = ' and '.join(["name like \'%{}%\'"] * len(keys))
        cmd = "select name from products where {}".format(cmd)
        # print cmd
        with self.connect:
            cur = self.connect.cursor()
            cur.execute(cmd.format(*keys))
            # 降二维为一维
            return list(itertools.chain.from_iterable(cur.fetchall()))
        return None

    def findPrices(self, key):
        cmd1 = "select sale from products where name like \'%{}%\'".format(key)
        cmd2 = "select save from products where name like \'%{}%\'".format(key)
        # print cmd1
        # print cmd2
        with self.connect:
            cur = self.connect.cursor()
            cur.execute(cmd1)
            # 降二维为一维
            sales = list(itertools.chain.from_iterable(cur.fetchall()))
            cur.execute(cmd2)
            saves = list(itertools.chain.from_iterable(cur.fetchall()))
            return (sales, saves)
        return None

if __name__ == "__main__":
    myutil.logging_init()
    cd = ChemistDatabase()
    cd.openDatabase()
    # print cd.searchName("swisse calcium")
    print cd.findProduct("Swisse Ultiboost Calcium + Vitamin D 150 Tablets")
    cd.closeDatabase()
    # cd.creatTable()
