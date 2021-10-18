""" Модуль для расчёта времени перелёта между точками
"""

from math import sqrt, hypot, cos, sin
from pprint import pprint
from typing import List

from data import *


def flying_time(i: int, j: int, points: List[tuple] = points, data: tuple = (Vfo, Vair, Beta)) -> float:
    """ Расчёт времени перелёта от точки i к точке j
    :param i: номер точки отправления
    :param j: номер точки прибытия
    :param points: список точек в формате (х, у)
    :param data: кортеж характеристик ЛА (скорость ЛА, воздушная скорость, угол скорости ветра)
    :return: время перелёта
    """

    Vfo, Vair, Beta = data

    if i == j:
        return float('inf')

    Xab = points[j][0] - points[i][0]
    Yab = points[j][1] - points[i][1]
    AB = hypot(Xab, Yab)
    Vair_x = Vair * cos(Beta)
    Vair_y = Vair * sin(Beta)
    t_ab = AB ** 2 / (sqrt(Vfo ** 2 * AB ** 2 - (Vair_x * Yab - Vair_y * Xab) ** 2) + Vair_x * Xab + Vair_y * Yab)

    return t_ab


def t_matrix(points: List[tuple] = points) -> List[List[float]]:
    matrix = []
    for i in range(n):
        matrix.append([0] * n)

    for i in range(n):
        for j in range(n):
            matrix[i][j] = round(flying_time(i=i, j=j), 5)

    return matrix


if __name__ == '__main__':
    pprint(t_matrix(points))
