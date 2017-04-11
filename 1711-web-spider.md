---
title: 使用网络爬虫抓取商品价格并分析
date: 2017-04-10
categories: python
tags: [embedded, linux, jz2440]
---


# 需求分析

基于 [Chemist Warehouse](http://www.chemistwarehouse.com.au/) 的商品, 抓取其每天的价格变化. 并根据历史信息, 判断其价格变化规律, 以便在打折时购买.

因此, 用户需求有如下几点:
- 抓取网站价格, 需要知道其商品全名, 原价, 打折价, 打折日期, 持续时间
- 存储这些数据, 供日后分析使用
- 数据挖掘和分析, 已直观的方式多维度显示出来(譬如单品的打折规律, 打折力度, 打折持续时间. 全年的打折规律)

进一步, 技术分析如下:
- 全程使用python即可满足全部需求.
- 网络爬虫难度不高, 仅需针对特定商品, 每天抓一次, 无需多线程/进程, 无需登录, 无验证码, 无需考虑反爬虫, 无需额外加载JS程序.
- 数据存储, 使用MySQL, 数据需要去重, 仅记录关键信息. 以便减少数据存储量, 简化数据挖掘和分析的工作
- 数据图表显示, 使用 matplotlib 即可.


最终源码见 [github](https://github.com/draapho/chemistwarehouse-spider)



# 网络爬虫

花了二天时间, 简单过了一遍网络爬虫的关键技术. 参考资料如下:
- [Python爬虫学习系列教程-静觅](http://cuiqingcai.com/1052.html)
- [Python入门网络爬虫之精华版](https://github.com/lining0806/PythonSpiderNotes)
- [XPath 语法](http://www.w3school.com.cn/xpath/xpath_syntax.asp)

本着项目导向, 做出结果为先的思路, 没有一步步的实验. 上来先看了几个爬虫框架.
- `pyspider` 基于web UI, 感觉很直观, 适合于随便玩玩. 个人不喜欢, 二次开发不方便.
- python 下另外一个很有名的框架就是 `scrapy`, 可惜我连配置安装都没有成功的做完. 适合二次开发.
  应该是公司网络安全机制比较高, 遇到的问题基本都是SSL相关的, 解决了2-3个, 剩下的实在没有思路去解决了...
  另外scrapy依赖的库也比较多, 因此初装也就比较麻烦. 安装推荐参考[官网的 Installation guide](https://docs.scrapy.org/en/latest/intro/install.html#)
- 使用 `requests` `urllib` `lxml` 库. 简单项目直接用这个就够了.
- 最终抓数据只用了 `lxml` 一个库就完成了数据抓取, 去重的工作. 关键源码如下:

``` python
# -*- coding:utf-8 -*-

from lxml import html

# 获取url的原始数据
doc = html.parse(url)
# 获取指定的数据值
names = doc.xpath('//a[@class="product-container search-result"]/@title')
# 处理数据, 准备存入数据库即可.
name = map(string.strip, names)
```

另:
遇到过了错误 `There was a problem confirming the ssl certificate: [SSL: CERTIFICATE_VERIFY_FAILED]`
使用 `pip --trusted-host pypi.python.org install lxml` 即可避免. 也是安全性问题导致的.


# 数据存储

同样地, 该项目对数据存储的要求也很低. 直接选择使用MySQL.

参考资料如下:
- [python操作mysql数据库](http://www.runoob.com/python/python-mysql.html)
- [Python操作Mysql实例代码教程（查询手册）](http://www.crazyant.net/686.html)
- [21分钟 MySQL 入门教程](http://www.cnblogs.com/mr-wid/archive/2013/05/09/3068229.html)

Windows 下配置使用MySQL:
- 下载运行 [MySQL Installer](https://dev.mysql.com/downloads/windows/)
- 必须安装 `MySQL Server`. 建议安装 `MySQL Workbench`, 为可视化图像, 便于管理查看.
- 将`mysql.exe`的路径添加`PATH`环境变量.
- 创建新的数据库(Workbecn下, 英文为`schema`), 命名为 `chemistwarehouse`. 或者输入指令:
  ``` bash
  mysql -u root -p      # 登录本机的MySQL数据库服务
  # mysql>              # 成功后, 提示符变为 mysql>
  create database chemistwarehouse; # 创建一个数据库
  ```
- 安装 [MySQL for Python](https://sourceforge.net/projects/mysql-python/)
  然后, 在python下面测试一下是否可以成功连接到刚建立的 `chemistwarehouse` 数据库.
  成功的话, 会打印版本信息.
  ``` python
  def initDatabase():
      try:
          # 连接mysql的方法：connect('ip','user','password','dbname')
          connect_db = db.connect(
              'localhost', 'root', 'root', 'chemistwarehouse')
          # 所有的查询，都在连接con的一个模块cursor上面运行的
          cur = connect_db.cursor()
          # 执行一个查询
          cur.execute("SELECT VERSION()")
          # 取得上个查询的结果，是单个结果
          data = cur.fetchone()
          print "Database version : %s " % data
      except Exception as e:
          logging.error(e)
      finally:
          if connect_db:
              # 无论如何，连接记得关闭
              connect_db.close()

  initDatabase()
  ```
- 至此, 就可以在python下正常使用MySQL数据库了.
  将提取出来的数据去重后, 按一定的格式保存进数据库即可.


# 数据显示





----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
