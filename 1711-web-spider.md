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
- 搜索指定产品, 展示历史数据, 使用 pyqt + matplotlib.


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
# pip --trusted-host pypi.python.org install lxml

import string
from lxml import html

# 获取url的原始数据
doc = html.parse('http://www.chemistwarehouse.com.au/search?searchtext=blackmores%20bone&searchmode=allwords')
# 获取指定的数据值
names = doc.xpath('//a[@class="product-container search-result"]/@title')
# 处理数据, 准备存入数据库即可.
name = map(string.strip, names)
print name
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
- [Windows下更改MySQL数据库的存储位置](http://blog.csdn.net/heizistudio/article/details/8234185)

Windows 下配置使用MySQL:
- 下载运行 [MySQL Installer](https://dev.mysql.com/downloads/windows/)
- 必须安装 `MySQL Server`. 建议安装 `MySQL Workbench`, 为可视化图像, 便于管理查看.
- 可视化工具也可以使用别的软件. 如 [heidisql](https://www.heidisql.com/)
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

- 默认安装在C盘, 而且数据存储也是在C盘. 这个没法接受! 需要把数据存储位置修改到空间更大的E盘.
  - 停止MySQL服务, 命令行 `net stop MySQL57` 或者使用 `MySQL Workbench` 停止服务
  - 打开 `C:\ProgramData\MySQL\MySQL Server 5.7\my.ini`
  - 修改为 `datadir=E:/MySQLdata`, 即设置数据库的新目录
  - 复制 `C:\ProgramData\MySQL\MySQL Server 5.7\Data` 下所有文件到 `E:/MySQLdata`
  - 开启MySQL服务 命令行 `net start MySQL57` 或者使用 `MySQL Workbench` 开启服务
  - 检查 MySQL 服务器状态, 确定数据库目录已更新
  - 删除 `C:\ProgramData\MySQL\MySQL Server 5.7\Data`


# 数据显示
参考资料如下:
- [Python 中用 matplotlib 绘制直方图](http://blog.topspeedsnail.com/archives/814) 这个博客有对 matplotlib 制图有一个系列的文章
- [用python的matplotlib库绘制柱状图和饼图](http://ningning.today/2015/04/17/python/%E7%94%A8matplotlib%E7%BB%98%E5%88%B6%E6%9F%B1%E7%8A%B6%E5%9B%BE%E5%92%8C%E9%A5%BC%E5%9B%BE/)
- [使用Python matplotlib绘制股票走势图](http://www.jdon.com/idea/matplotlib.html)
- [Building a Matplotlib GUI with Qt Designer: Part 1](http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-1/), 由三部分组成, 还有[Part2](http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-2/)和[Part3](http://blog.rcnelson.com/building-a-matplotlib-gui-with-qt-designer-part-3/)
- [matplotlib with PyQt GUIs](http://eli.thegreenplace.net/2009/01/20/matplotlib-with-pyqt-guis), 有 [github 范例](https://github.com/eliben/code-for-blog/blob/master/2009/qt_mpl_bars.py)
- pyqt的使用可参考我的博客 [python的第一个小程序, 蓝牙及串口终端](https://draapho.github.io/2016/11/16/1617-python-terminal/)

设计思路和注意事项
- 使用pip安装 matplotlib: `pip --trusted-host pypi.python.org install matplotlib`
- 数据显示和数据抓取是完全独立的, 因此数据抓取单独生成了一个exe文件, 数据显示也单独生成一个文件.
- 数据显示exe可以打开多个, 以便分析比较. 数据抓取仅可打开一个.


# 源码及性能
最终源码见 [github](https://github.com/draapho/chemistwarehouse-spider)

爬虫最终性能:
抓取效率一般, 每1000条数据大概要2分钟. 要提高效率可以考虑使用多进程!
但一天抓取一次即可, 因此这个速度可以接受. 暂时保持单进程不变.


----------

***原创于 [DRA&PHO](https://draapho.github.io/)***
