# coding=utf-8

# pip --trusted-host pypi.python.org install numpy
# pip --trusted-host pypi.python.org install matplotlib
# pyuic4.bat -x -o gui.py gui.ui
# pyinstaller.exe --onefile --windowed gui_action.py

import gui
import sys
import numpy as np
from PyQt4.QtGui import QApplication, QMainWindow
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)


class GuiAction(QMainWindow, gui.Ui_MainWindow):

    def __init__(self, ):
        super(self.__class__, self).__init__()
        self.setupUi(self)

    def addmpl(self, fig):
        self.canvas = FigureCanvas(fig)
        self.verticalLayoutDraw.addWidget(self.canvas)
        self.canvas.draw()
        self.toolbar = NavigationToolbar(
            self.canvas, self.widgetDraw, coordinates=True)
        self.verticalLayoutDraw.addWidget(self.toolbar)

if __name__ == '__main__':
    fig1 = Figure()
    ax1f1 = fig1.add_subplot(111)
    ax1f1.plot(np.random.rand(5))

    app = QApplication(sys.argv)
    main = GuiAction()
    main.addmpl(fig1)
    main.show()
    sys.exit(app.exec_())
