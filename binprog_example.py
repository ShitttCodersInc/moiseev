from cvxopt import glpk
import cvxopt

f = [-9, -5, -6, -4]
A = [[6, 3, 5, 2], [0, 0, 1, 1], [-1, 0, 1, 0], [0, -1, 0, 1]]
b = [9, 1, 0, 0]

c = cvxopt.matrix(f, tc='d')
G = cvxopt.matrix(A, tc='d')
h = cvxopt.matrix([9, 1, 0, 0], tc='d')

(status, x) = glpk.ilp(c=c, G=G.T, h=h, B=set(range(len(f))))
print(status)
print(x)

# print(sum(c.T * x))
