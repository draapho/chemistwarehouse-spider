# coding=utf-8

# pip --trusted-host pypi.python.org install numpy
# pip --trusted-host pypi.python.org install matplotlib
# pyuic4.bat -x -o gui.py gui.ui
# pyinstaller.exe --onefile --windowed gui_action.py

import gui
import sys
import os
import myutil
import ChemistSpider
from ChemistDatabase import ChemistDatabase
from ChemistServer import LOG_FILE
from PyQt4.QtGui import QApplication, QMainWindow
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class GuiAction(QMainWindow, gui.Ui_MainWindow):

    def __init__(self, ):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        # Input Area
        self.pushButtonOpen.clicked.connect(self.open_logging)
        self.pushButtonClear.clicked.connect(self.clear_diagram)
        self.comboBoxProduct.currentIndexChanged.connect(self.input_changed)
        self.comboBoxProduct.setCurrentIndex(0)
        self.categories = ["Search"]
        for url in ChemistSpider.CATEGORIES:
            self.categories.append("category " + url.split('/')[-1])
        self.comboBoxProduct.addItems(self.categories)
        self.list_len = len(self.categories)

    # 加载logging文件
    # def read_logging(self):
    #     with open(LOG_FILE) as f:
    #         for line in f:
    #             color = 'red' if "ERROR" in line else 'grey'
    #             val = "<font color={}>{}</font>".format(color, line)
    #             self.textBrowserLog.moveCursor(QTextCursor.End)
    #             self.textBrowserLog.append(val)
    #         self.textBrowserLog.moveCursor(QTextCursor.End)
    #         self.textBrowserLog.append("")

    def open_logging(self):
        os.startfile(LOG_FILE)

    def clear_diagram(self):
        for i in reversed(range(self.verticalLayoutDraw.count())):
            self.verticalLayoutDraw.takeAt(i).widget().setParent(None)

    def input_changed(self):
        if self.comboBoxProduct.currentIndex() <= 0:
            pass
        elif self.comboBoxProduct.currentIndex() < self.list_len:
            # get product, show diagram
            name = myutil.trim_str(
                str(self.comboBoxProduct.currentText().toUtf8()))
            if "category " in name:
                db = ChemistDatabase()
                db.openDatabase()
                totals = db.findProduct("category-total " + name.split()[-1])
                counts = db.findProduct("category-count " + name.split()[-1])
                db.closeDatabase()
                self.creatDiagramCategory(totals, counts)
            else:
                db = ChemistDatabase()
                db.openDatabase()
                product = db.findProduct(name)
                db.closeDatabase()
                self.creatDiagramProduct(product)
        else:
            # search product
            search = myutil.trim_str(
                str(self.comboBoxProduct.currentText().toUtf8()))
            if search == "":
                self.comboBoxProduct.clear()
                self.comboBoxProduct.addItems(self.categories)
                self.list_len = len(self.categories)
            else:
                db = ChemistDatabase()
                db.openDatabase()
                names = db.searchName(search)
                db.closeDatabase()
                self.comboBoxProduct.clear()
                self.comboBoxProduct.addItem("Select or Search")
                self.comboBoxProduct.addItems(names)
                self.list_len = len(names) + 1

    def creatDiagramCategory(self, totals, counts):
        # basic setting
        fig = Figure()
        axis = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        self.verticalLayoutDraw.addWidget(canvas)
        toolbar = NavigationToolbar(canvas, self.widgetDraw)
        self.verticalLayoutDraw.addWidget(toolbar)
        # cook data
        name = "category " + str(totals[1][0]).split()[-1]
        x = totals[2]
        count_ratio = [round(j / i, 2) for i in counts[3] for j in counts[4]]
        price_ratio = [round(i / (i + j), 2) for i in totals[3] for j in totals[4]]
        # 设置x轴为日期
        try:
            date_range = (x[-1] - x[1]).days
        except:
            date_range = 0
        axis.xaxis.set_major_locator(
            mdates.DayLocator(interval=(1 + date_range // 12)))
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d -%a"))
        axis.set_title(name)
        y1, = axis.plot(x, count_ratio, 'xg-', label='line1')
        y2, = axis.plot(x, price_ratio, '+r-', label='line2')
        axis.legend([y1, y2], ['save/total count', 'sale/total $'], loc=1)
        fig.autofmt_xdate()

    def creatDiagramProduct(self, product):
        # basic setting
        fig = Figure()
        axis = fig.add_subplot(111)
        canvas = FigureCanvas(fig)
        self.verticalLayoutDraw.addWidget(canvas)
        toolbar = NavigationToolbar(canvas, self.widgetDraw)
        self.verticalLayoutDraw.addWidget(toolbar)
        # cook data
        name = str(product[1][0])
        # x = [datetime.datetime.strptime(d, '%Y-%m-%d').date() for d in product[2]]
        x = product[2]
        sale = product[3]
        save = product[4]
        total = [i + j for i in sale for j in save]
        # 设置x轴为日期
        try:
            date_range = (x[-1] - x[1]).days
        except:
            date_range = 0
        axis.xaxis.set_major_locator(
            mdates.DayLocator(interval=(1 + date_range // 12)))
        axis.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d -%a"))
        axis.set_title(name)
        y1, = axis.plot(x, total, '+k--', label='line1')
        y2, = axis.plot(x, sale, 'or-', label='line2')
        y3, = axis.plot(x, save, 'xg-', label='line3')
        axis.legend([y1, y2, y3], ['sale', 'save', 'total'], loc=4)
        fig.autofmt_xdate()

if __name__ == '__main__':
    # myutil.logging_init()
    app = QApplication(sys.argv)
    gui_action = GuiAction()
    gui_action.show()
    sys.exit(app.exec_())
