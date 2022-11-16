import sys
import timeit
from datetime import datetime
from time import sleep, time

import pyqtgraph
from PyQt5 import QtWidgets

import mainGUI2 as mainGUI
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
        accuracy = self.ui.inputValuesAccuracy.value() / 100


        # Генерируем списки для дальнейшей записи в них значений Х и У.
        Xs = []
        Ys = []
        lastSum = 0             # для алгоритма бинарного поиска, работа всегда в меньшую сторону.
        step = end - start      # стартовый шаг биения задаём как всю длину графика.

        # Атрибуты для алгоритма.
        run = True
        iterations = 0
        delta_accuracy = 0      # Расхождение погрешности на каждой итерации.

        # Пока запущен цикл, шаг каждый раз бьётся пополам и по нему вычисляется итоговая сумма интеграла.
        # По факту - увеличиваем детализацию биения графика, пока delta_accuracy не станет меньше погрешности пользователя.
        while run:
            step = step / 2
            curSum = 0
            iterations = iterations +1

            # Генерируем список из точек Х с шагом step.
            Xs = generate_Xs(start, end, step)

            # Для каждой точки из списка Xs генерим значение y = f(x)
            Ys = [f(x) for x in Xs]

            # Считываем желаемый метод расчёта и в соответствии ему запускаем требуемый метод.
            if self.ui.radioButton_LeftSqr.isChecked():
                curSum = method_leftSqr(Xs, step)
                # print("Debug", curSum)

            elif self.ui.radioButton_trapezoid.isChecked():
                curSum = method_trp(Xs, step)

            elif self.ui.radioButton_Simpson.isChecked():
                curSum = method_Simpson(Xs, step)

            delta_accuracy = abs(curSum - lastSum)
            if  delta_accuracy <= accuracy:
                run = False

            lastSum = curSum

            print(iterations)


        # Рисуем график, который в будущем будет проинтегрирован.
        self.ui.graphicsView.plot(Xs, Ys, pen=self.penMeinGraph)

        # Считаем общее количество итераций как количество точек X.
        timer = time()      # посмотрим, прав ли Евгений Александрович на счёт быстродействия Симпсона >:)

        # # Считаем время выполнения кода и выводим его на экран.
        # timer_delay = time() - timer
        # self.ui.lcd_lostTime.display(timer_delay)

        # Поступаем также с итоговым значением интеграла.
        self.ui.lcd_iterations.display(iterations)
        self.ui.lsd_integrals.display(lastSum)

        # Отобразим значение погрешности.
        self.ui.lcd_iterations_2.display(delta_accuracy * 100)

        # Для наглядности степени детализации - отобразим гистограмму точек, соовтетствующих биению графика.
        gP = generate_gistograms(Xs, step)
        self.ui.graphicsView.plot(gP[0], gP[1], pen=(1, 1))


# Главная точка входа, отсюда запускается работа всего приложения.
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWindow()
    ui.dialog.show()
    sys.exit(app.exec_())