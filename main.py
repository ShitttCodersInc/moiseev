from time import time
from typing import List

import cvxopt
import numpy as np
from cvxopt import glpk

import flight_time
import output
import restrictions
import subcycle
from data import *

glpk.options['msg_lev'] = 'GLP_MSG_OFF'
restrictions_list = []

find_criterion = lambda x, t_matrix: sum([t_matrix[i][j] for i in range(n) for j in range(n) if x[i][j]])


# Добавить ограничение в текстовом виде в restrictions_list
def add_restriction_to_list(_p: List[tuple]) -> None:
    _p_str = f'x{_p[0][0] + 1}{_p[0][1] + 1}'
    for pair in range(1, len(_p)):
        _p_str += f' + x{_p[pair][0] + 1}{_p[pair][1] + 1}'
    _p_str += f' <= {len(_p) - 1}'
    restrictions_list.append(_p_str)


def main():
    restrictions.init_restrictions()
    t_matrix = flight_time.t_matrix()
    C = np.array(t_matrix).reshape(n ** 2)
    c = cvxopt.matrix(C, tc='d')

    time_start = time()
    while True:
        # A * x = b
        A = cvxopt.matrix(restrictions.A, tc='d')
        b = cvxopt.matrix(restrictions.b, tc='d')

        # G * x <= h
        G = cvxopt.matrix(restrictions.G, tc='d')
        h = cvxopt.matrix(restrictions.h, tc='d')

        # Найти оптимальное решение
        (status, x) = glpk.ilp(c=c, G=G.T, h=h, A=A.T, b=b, B=set(range(len(C))))

        # Матрица перелетов
        x = np.array(list(x)).reshape(n, n)

        # Значение критерия (время облёта)
        s = find_criterion(x, t_matrix)

        print('Матрица облёта')
        print(x)
        print('Время облёта:', s)

        # Найти подциклы
        cycles, cycles_index = subcycle.find_subcycles(x=x)

        # Вывести картинку на экран
        output.output(_points=cycles, criterion=s, p_indexes=cycles_index)

        # Если подцикл 1, то это решение
        if len(cycles) == 1:
            print('\n===== дополнительные ограничения ======')
            for r in restrictions_list:
                print(r)
            print('ВСЕГО:', len(restrictions_list))

            plan = '-'.join(map(str, cycles_index[0])) + '; '
            output.log_output(restrictions=restrictions_list, x=x, criterion=s, elapsed_time=time() - time_start,
                              plan=plan)
            break

        for indexes in cycles_index:
            # Получить набор значений (i, j) для облета
            _p = restrictions.parse_subcycle_indexes(indexes)

            # Запомнить ограничение в текстовом виде
            add_restriction_to_list(_p=_p)

            # Добавить ограничения для исключения подциклов
            restrictions.add_restriction(_p)


if __name__ == '__main__':
    main()
