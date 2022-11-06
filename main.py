import sys
import timeit
from datetime import datetime
from time import sleep, time

import pyqtgraph
from PyQt5 import QtCore, QtWidgets, QtGui
import src

import mainGUI
from maths import *

# Создание класса для GUI окна.
class mainWindow(QtWidgets.QMainWindow):
    def __init__(self):

        # Инициализация.
        super().__init__()
        self.dialog = QtWidgets.QDialog()
        self.ui = mainGUI.Ui_Dialog()
        self.ui.setupUi(self.dialog)

        # Подключаем сигнал клика главной кнопки к функции рисования графиков.
        self.ui.pushButtonRun.clicked.connect(self.drawGraph)

        # Ништяки по кастомизации графиков
        self.ui.graphicsView.setBackground('w')                     # установка цвета фона
        self.ui.graphicsView.showGrid(1, 1, 1)                      # включаем сетку
        self.penMeinGraph = pyqtgraph.mkPen(color='g', width=3)     # устанавливаем красоту интегрируемого графика


    def drawGraph(self):
        """
        Главная функуия отображения графиков
        :return:
        """

        # Очищаем поле графика от предыдущих художеств.
        self.ui.graphicsView.clear()

        # Считываем значения с полей пользователя.
        start = self.ui.inputValuesFrom.value()
        end = self.ui.inputValuesTo.value()
        step = self.ui.inputValuesStep.value()

        # Генерируем список из точек Х с шагом step.
        Xs = generate_Xs(start, end, step)

        # Для каждой точки из списка Xs генерим значение y = f(x)
        Ys = [f(x) for x in Xs]

        # Рисуем график, который в будущем будет проинтегрирован.
        self.ui.graphicsView.plot(Xs, Ys, pen=self.penMeinGraph)
        # print(Ys)

        # Считаем общее количество итераций как количество точек X.
        iteration = len(Ys)
        sum = 0             # итоговое значение интеграла.
        timer = time()      # посмотрим, прав ли Евгений Александрович на счёт быстродействия Симпсона >:)


        # Считываем желаемый метод расчёта и в соответствии ему запускаем требуемый метод.
        if self.ui.radioButton_LeftSqr.isChecked():
            sum = method_leftSqr(Xs, step)

        elif self.ui.radioButton_CenterSqr.isChecked():
            sum = method_centerSqr(Xs, step)

        elif self.ui.radioButton_Simpson.isChecked():
            sum = method_Simpson(Xs, step)

        # Считаем время выполнения кода и выводим его на экран.
        timer_delay = time() - timer
        self.ui.lcd_lostTime.display(timer_delay)

        # Поступаем также с итоговым значением интеграла.
        self.ui.lcd_iterations.display(iteration)
        self.ui.lsd_integrals.display(sum)


        # Для наглядности степени детализации - отобразим гистограмму точек, соовтетствующих биению графика.
        gP = generate_gistograms(Xs, step)
        self.ui.graphicsView.plot(gP[0], gP[1], pen=(1, 1))


# Главная точка входа, отсюда запускается работа всего приложения.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.dialog.show()
    sys.exit(app.exec_())