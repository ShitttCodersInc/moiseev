""" Вывод результатов
Описан метод для вывода маршрута облета точек
"""

import matplotlib.pyplot as plt
from typing import List
from data import points
import datetime
import os
import numpy as np

now = datetime.datetime.now()
chart = 0
FOLDER = 'data'
SUBFOLDER = '{:02}{:02}{:02}{:02}{:02}{:02}'.format(now.hour, now.minute, now.second, now.day, now.month, now.year)
DATAPATH = f'{FOLDER}/{SUBFOLDER}'


def output(_points: List[List[tuple]], criterion: float = -1, p_indexes: List[List[int]] = []) -> None:
    """ Вывести график
    Отрисовывает на 2D графике маршрут облёта
    :param p_indexes: список номеров точек облёта
    :param _points: список кортежей с координатами точек формата (x,y)
    :param criterion: минимизируемый критерий (время облёта)
    :return:
    """
    global chart
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    for i in range(len(_points)):
        __points = _points[i]
        __p_indexes = p_indexes[i]

        x = [px for px, _ in __points]
        y = [py for _, py in __points]

        for px, py in __points:
            # plt.text(px, py, f'P{points.index((px, py)) + 1}: ({px};{py}) - {__points.index((px, py)) + 1}')
            plt.text(px, py, f'P{points.index((px, py)) + 1}')
            plt.plot(px, py, 'r.')

        plt.plot(x, y)

    plt.grid()
    plt.xlabel('X, km')
    plt.ylabel('Y, km')
    s = ''
    for ind in p_indexes:
        s += '→'.join(map(str, ind)) + '; '
    plt.title(f'Время облёта: {criterion} часов\n Маршрут: {s}')
    chart += 1
    plt.savefig(f'{DATAPATH}/{chart}.png')
    plt.show()


def log_output(restrictions: List[str], x: np.ndarray, criterion: float, elapsed_time: float, plan: str) -> None:
    if not os.path.exists(FOLDER):
        os.mkdir(FOLDER)
    if not os.path.exists(DATAPATH):
        os.mkdir(DATAPATH)

    with open(f'{DATAPATH}/log.txt', 'w') as file:
        file.write(f'План полёта: {plan}\n')
        file.write(f'Значение критерия: {criterion} час\n\n')
        file.write('Матрица облёта\n')
        file.write(str(x))
        file.write(f'\n\nДоп ограничения для исключения подциклов (ВСЕГО: {len(restrictions)})\n')

        for r in restrictions:
            file.write(f'{r}\n')

        file.write(f'\nВремя построения маршрута: {elapsed_time} сек')


if __name__ == '__main__':
    _points = [(1, 1), (3, 3), (1, 3), (1, 1)]
    output(_points, 345)
