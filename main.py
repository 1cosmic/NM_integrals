import sys
import timeit
from datetime import datetime
from time import sleep, time

import pyqtgraph
from PyQt5 import QtCore, QtWidgets, QtGui
import src

import mainGUI
from maths import *


class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.dialog = QtWidgets.QDialog()
        self.ui = mainGUI.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        self.ui.pushButtonRun.clicked.connect(self.drawGraph)
        self.ui.graphicsView.setBackground('w')
        self.ui.graphicsView.showGrid(1, 1, 1)
        self.penMeinGraph = pyqtgraph.mkPen(color='g', width=3)

    def drawGraph(self):

        start = self.ui.inputValuesFrom.value()
        end = self.ui.inputValuesTo.value()
        step = self.ui.inputValuesStep.value()

        self.ui.graphicsView.clear()
        Xs = generate_Xs(start, end, step)
        Ys = [f(x) for x in Xs]
        self.ui.graphicsView.plot(Xs, Ys, pen=self.penMeinGraph)
        # print(Ys)

        iteration = len(Ys)
        sum = 0
        timer = time()

        if self.ui.radioButton_LeftSqr.isChecked():
            sum = method_leftSqr(Xs, step)

        elif self.ui.radioButton_CenterSqr.isChecked():
            sum = method_centerSqr(Xs, step)

        elif self.ui.radioButton_Simpson.isChecked():
            sum = method_Simpson(Xs, step)

        timer_delay = time() - timer
        self.ui.lcd_lostTime.display(timer_delay)

        self.ui.lcd_iterations.display(iteration)
        self.ui.lsd_integrals.display(sum)


        gP = generate_gistograms(Xs, step)
        self.ui.graphicsView.plot(gP[0], gP[1], pen=(1, 1))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.dialog.show()
    sys.exit(app.exec_())
