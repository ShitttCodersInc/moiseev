""" Процедура для нахождения подцикла

"""

from data import *
import numpy as np


def find_subcycles(x: np.ndarray, start_point: int = 0) -> tuple:
    p = [points[start_point]]
    subcycles = []
    subcycles_indexes = []
    indexes = [start_point + 1]
    p_index = start_point
    p_flag = [False] * n

    while not all(p_flag):
        for j in range(n):
            if x[p_index][j] == 1:
                p_flag[j] = True
                p.append(points[j])
                indexes.append(j + 1)
                p_index = j
                if p_index == start_point:
                    # Запомнить подцикл
                    subcycles.append(p)
                    subcycles_indexes.append(indexes)

                    # найти новую точку старта
                    for c in range(n):
                        if not p_flag[c]:
                            start_point = c
                            p = [points[start_point]]
                            indexes = [c + 1]
                            p_index = start_point
                            break

                break
    if not subcycles:
        # p.append(p[0])
        # indexes.append(indexes[0])
        subcycles.append(p)
        subcycles_indexes.append(indexes)
    return subcycles, subcycles_indexes
