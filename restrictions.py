""" Модуль для формирования ограничений
Ограничения типа =      A*x = b
Ограничения типа <=     G*x <= h
"""

from typing import List
from data import *

A = []
b = []
G = []
h = []


def init_restrictions(_n: int = n):
    """Сформировать начальные органичения
    сумма по строкам = 1
    сумма по таблицам = 1
    :param _n: общее количество точек
    """
    # Ограничения на строки
    for i in range(_n):
        left = [0] * _n ** 2
        right = 1

        for j in range(_n):
            if i != j:
                left[i * _n + j] = 1

        A.append(left)
        b.append(right)

    # Ограничения на столбцы
    for j in range(_n):
        left = [0] * _n ** 2
        right = 1

        for i in range(_n):
            if i != j:
                left[i * _n + j] = 1

        A.append(left)
        b.append(right)

    left = [0] * _n ** 2
    right = 1

    # 1->2->1
    left[0 * _n + 1] = 1
    left[1 * _n + 0] = 1

    G.append(left)
    h.append(right)


def add_restriction(points_indexes: List[tuple], _n: int = n):
    """ Добавить ограничения типа неравенства для исключения подциклов
    :param _n: общее количество точек
    :param points_indexes: список кортежей номеров точек в формате (i, j)
    :return:
    """
    left = [0] * _n ** 2
    right = len(points_indexes) - 1

    for i, j in points_indexes:
        left[i * _n + j] = 1

    G.append(left)
    h.append(right)


def parse_subcycle_indexes(points_numbers: List[int], _n: int = n):
    p_list = []
    for c in range(len(points_numbers) - 1):
        p_list.append((points_numbers[c] - 1, points_numbers[c + 1] - 1))
    return p_list


if __name__ == '__main__':
    init_restrictions()
    print(A)
    print(b)
    add_restriction([(0, 1), (1, 2), (2, 0)])
    print(G)
    print(h)
