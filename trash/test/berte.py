from z3 import *
import numpy as np
from math import ceil
from time import process_time
from utility import *


instance = 1
rotation = True  # Flag to handle rotation

path = 'C:/Users/Mattia/Desktop/cdmo project/instances/'
ins = 'ins-{}.txt'.format(instance)
t_max = 300000  # milliseconds
W, n, dimensions = read_data(path + ins)


t_start = process_time()

# Decreasing area ordering
area = [int(dimensions[i][0]*dimensions[i][1]) for i in range(0, len(dimensions))]
neg_area = [-int(area[i]) for i in range(len(dimensions))]
order = np.argsort(neg_area)

opt = Optimize()
opt.set('timeout', t_max)

# Coordinates variables
x = [Int("x_%s" % i)for i in range(n)]
y = [Int("y_%s" % i)for i in range(n)]

# Height variable to minimize
H = Int('H')
h_min = ceil(sum(area)/W)
opt.add(H >= h_min)
h_max = 2*h_min
opt.add(H <= h_max)

if not rotation:

    w = [int(dimensions[i][0]) for i in order]
    h = [int(dimensions[i][1]) for i in order]

    # Height variable to minimize
    H = Int('H')

    # Containment constraint
    cont_row = [And(0 <= x[i], x[i]+w[i] <= W) for i in range(n)]
    cont_col = [And(0 <= y[i], y[i]+h[i] <= H) for i in range(n)]
    opt.add(cont_row)
    opt.add(cont_col)

    # No overlapping constraint
    no_overlapping = [Or(i == j, Or(x[i]+w[i] <= x[j], x[j]+w[j] <= x[i],
                     y[i]+h[i] <= y[j], y[j]+h[j] <= y[i])) for i in range(n) for j in range(n)]
    opt.add(no_overlapping)

    # Cumulative constraints
    sum_h = [0 for i in range(W)]
    for i in range(W):
        for j in range(n):
            if x[j] == i:
                sum_h[i] += h[j]
        opt.add(sum_h[i] < H)

    sum_w = [0 for i in range(round(h_max))]
    for i in range(round(h_max)):
        for j in range(n):
            if y[j] == i:
                sum_w[i] += w[j]
        opt.add(sum_w[i] < W)

    # Symmetry breaking constraint
    sym1 = [And(x[0] <= 1 + (W-w[0])/2, y[0] <= 1 + (H-h[0])/2)]
    opt.add(sym1)

    opt.minimize(H)

    check = opt.check()
    model = opt.model()

    t_stop = process_time()
    delta_t = t_stop - t_start

    if check == sat:
        print('Optimal solution found in {:.3f}'.format(delta_t))
        print('H = {}'.format(model.evaluate(H)))

        out_name, output_file = output(ins, model, order, W, H, n, w, h, x, y)
        print('Results saved in file \'{}\''.format(out_name))
        display_sol(out_name)

    else:
        print('No optimal solution found')

if rotation:

    # Height and W variables
    w = [Int("w_%s" % i) for i in range(n)]
    h = [Int("h_%s" % i) for i in range(n)]

    # Variables to handle rotation
    r = [Int("r_%s" % i) for i in range(n)]

    # Rotation constraint
    rot = [Or(r[i] == 0, r[i] == 1) for i in range(n)] # Makes r a binary variable
    rot_w = [w[i] == (1 - r[i]) * dimensions[i][0] + r[i] * dimensions[i][1] for i in range(n)]
    rot_h = [h[i] == r[i] * dimensions[i][0] + (1 - r[i]) * dimensions[i][1] for i in range(n)]
    opt.add(rot)
    opt.add(rot_w)
    opt.add(rot_h)

    # Containment constraint
    cont_row = [And(0 <= x[i], x[i] + w[i] <= W) for i in range(n)]
    cont_col = [And(0 <= y[i], y[i] + h[i] <= H) for i in range(n)]
    opt.add(cont_row)
    opt.add(cont_col)

    # No overlapping constraint
    no_over = [Or(i == j, Or(x[i] + w[i] <= x[j], x[j] + w[j] <= x[i], y[i] + h[i] <= y[j], y[j] + h[j] <= y[i]))
               for i in range(n) for j in range(n)]
    opt.add(no_over)

    # Cumulative constraint
    sum_h = [0 for i in range(W)]
    for i in range(W):
        for j in range(n):
            if x[j] == i:
                sum_h[i] += h[j]
        opt.add(sum_h[i] < H)

    sum_w = [0 for i in range(round(h_max))]
    for i in range(round(h_max)):
        for j in range(n):
            if y[j] == i:
                sum_w[i] += w[j]
        opt.add(sum_w[i] < W)

    # Symmetry breaking constraints
    sym1 = [And(x[0] <= 1 + (W - w[0]) / 2, y[0] <= 1 + (H - h[0]) / 2)]
    opt.add(sym1)
    # No rotation for square circuits
    no_rot = [Or(w[i] != h[i], r[i] == 0) for i in range(n)]
    opt.add(no_rot)
    # When two circuits have the same dimensions but swapped, it avoids
    # to rotate both and obtain the same circuits
    sym2 = [Implies(And(dimensions[i][0] == dimensions[j][1], dimensions[i][1] == dimensions[j][0]),
                    Not(And(r[i] == 1, r[j] == 1))) for i in range(n) for j in range(n)]
    opt.add(sym2)

    opt.minimize(H)

    check = opt.check()
    model = opt.model()

    t_stop = process_time()
    delta_t = t_stop - t_start

    if check == sat:
        print('Optimal solution found in {:.3f}'.format(delta_t))
        print('H = {}'.format(model.evaluate(H)))

        out_name, output_file = output_rot(ins, model, order, W, H, n, w, h, x, y)
        print('Results saved in file \'{}\''.format(out_name))
        display_sol(out_name)

    else:
        print('No solution found within time limit.')