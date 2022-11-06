from math import sin

from numpy import arange


def f(x):
    '''
    Исходный график функции.

    :param x:
    :return:
    '''
    return sin(x)


def generate_Xs(start, end, step):
    '''
    Генерация точек X.

    :param start:
    :param end:
    :param step:
    :return:
    '''
    points = [i for i in arange(start, end, step)]
    # print(end)
    points.append(end)

    return points


def method_leftSqr(Xs, step):
    """
    Метод левосторонних прямоугольников.

    :param Xs:
    :param step:
    :return:
    """

    sum = 0

    for x in Xs:
        sum += f(x) * step

    return sum


def method_centerSqr(Xs, step):
    """
    Метод серединных прямоугольников.

    :param Xs:
    :param step:
    :return:
    """
    sum = 0

    for x in Xs:
        sum += f(x - step / 2) * step

    return sum


def method_Simpson(Xs, step):
    """
    Метод Симпсона.

    :param Xs:
    :param step:
    :return:
    """
    # row = Xs[1:len(Xs) -1]
    sum_x1 = 0
    sum_x2 = 0
    integral = 0

    for i in range(len(Xs))[2::2]:

        sum_x1 = sum_x1 + f(Xs[i - 1])
        sum_x2 = sum_x2 + f(Xs[i])

        # print(i-1, i)

    else:
        integral = (step / 3) * (Xs[0] + 4 * sum_x1 + 2 * (sum_x2) + Xs[-1])

    return integral


def generate_gistograms(Xs, step):
    """
    Генерация графика гистограмм.

    :param Xs:
    :param step:
    :return:
    """

    gistoPoints = [], []

    for x in Xs[:len(Xs) -1]:
        for i in range(2):
            gistoPoints[0].append(x + step * i)
            gistoPoints[1].append(f(x) * i)

            gistoPoints[0].append(x + step * i)
            gistoPoints[1].append(f(x))


    return gistoPoints