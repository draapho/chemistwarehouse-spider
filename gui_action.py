# coding=utf-8

# pip --trusted-host pypi.python.org install numpy
# pip --trusted-host pypi.python.org install matplotlib
# pyuic4.bat -x -o gui.py gui.ui
# pyinstaller.exe --onefile --windowed gui_action.py

import gui
import sys
import os
import logging
import myutil
import ChemistSpider
import numpy
from ChemistDatabase import ChemistDatabase
from ChemistServer import LOG_FILE
from PyQt4.QtGui import QApplication, QMainWindow, QStandardItemModel, QStandardItem
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
        self.comboBoxProduct.currentIndexChanged.connect(self.input_changed)
        self.comboBoxProduct.setCurrentIndex(0)
        self.categories = [""]
        for url in ChemistSpider.CATEGORIES:
            self.categories.append("category " + url.split('/')[-1])
        self.comboBoxProduct.addItems(self.categories)
        self.list_len = len(self.categories)

        # get and add all product's name
        # db = ChemistDatabase.ChemistDatabase()
        # db.openDatabase()
        # names = db.searchName()
        # db.closeDatabase()
        # self.comboBoxProduct.addItems(names)

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

    def input_changed(self):
        if self.comboBoxProduct.currentIndex() <= 0:
            pass
        elif self.comboBoxProduct.currentIndex() < self.list_len:
            # get product, show diagram
            name = myutil.trim_str(str(self.comboBoxProduct.currentText()))
            if "category " in name:
                pass
            else:
                db = ChemistDatabase()
                db.openDatabase()
                product = db.findProduct(name)
                db.closeDatabase()
                print product # ////////////////////
        else:
            # search product
            search = myutil.trim_str(str(self.comboBoxProduct.currentText()))
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
                self.comboBoxProduct.addItem("")
                self.comboBoxProduct.addItems(names)
                self.list_len = len(names) + 1

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.verticalLayoutDraw.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(
            self.canvas, self.widgetDraw, coordinates=True)
        self.verticalLayoutDraw.addWidget(self.toolbar)

if __name__ == '__main__':
    myutil.logging_init()

    fig1 = Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(numpy.random.rand(5))

    app = QApplication(sys.argv)
    main = GuiAction()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
