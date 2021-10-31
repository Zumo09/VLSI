import argparse
from time import process_time

import numpy as np
from z3 import *

from visualize import visualize_instance


def run_instance(instance: int, allow_rotation=False, timeout=5, visualize=True):
    # Read instance data
    with open(f'../instances/ins-{instance}.txt', 'r') as file:
        lines = file.readlines()

    width = int(lines[0])
    n = int(lines[1])
    chip_w = []
    chip_h = []

    for i in range(2, 2 + n):
        w, h = lines[i].split()
        chip_w.append(int(w))
        chip_h.append(int(h))

    print(f'Running instance {instance}{" with rotation allowed " if allow_rotation else " "}'
          f'(timeout {timeout} min)')

    area = [chip_w[i] * chip_h[i] for i in range(n)]
    max_area_idx = np.argmax(area)

    opt = Optimize()
    opt.set('timeout', timeout * 60000)

    # Coordinates variables
    x = [Int(f'x_{i}') for i in range(n)]
    y = [Int(f'y_{i}') for i in range(n)]

    # Objective
    height = Int('height')

    # minimum and maximum height
    h_min_area = np.ceil(np.sum(area) / width)
    h_min = max(np.max(chip_h), h_min_area)
    h_min = int(h_min)
    h_max = 2 * h_min

    opt.add(height >= h_min)
    opt.add(height <= h_max)

    if allow_rotation:
        # Height and width variables
        w = [Int(f'w_{i}') for i in range(n)]
        h = [Int(f'h_{i}') for i in range(n)]

        # Variables to handle rotation
        r = [Int(f'r_{i}') for i in range(n)]

        # Rotation constraint
        opt.add([Or(r[i] == 0, r[i] == 1) for i in range(n)])  # Makes r a binary variable
        opt.add([w[i] == (1 - r[i]) * chip_w[i] + r[i] * chip_h[i] for i in range(n)])
        opt.add([h[i] == r[i] * chip_w[i] + (1 - r[i]) * chip_h[i] for i in range(n)])

        # No rotation for square circuits
        opt.add([Or(w[i] != h[i], r[i] == 0) for i in range(n)])
        # When two circuits have the same dimensions but swapped, it avoids
        # to rotate both and obtain the same circuits
        opt.add([Implies(And(chip_w[i] == chip_h[j], chip_h[i] == chip_w[j]),
                         Not(And(r[i] == 1, r[j] == 1))) for i in range(n) for j in range(n)])
    else:
        w = chip_w
        h = chip_h

    # No overlapping constraint
    opt.add([Or(x[i] + w[i] <= x[j], x[j] + w[j] <= x[i],
                y[i] + h[i] <= y[j], y[j] + h[j] <= y[i])
             for i in range(n) for j in range(n) if i < j])

    # Containment constraint
    opt.add([And(0 <= x[i], x[i] + w[i] <= width) for i in range(n)])
    opt.add([And(0 <= y[i], y[i] + h[i] <= height) for i in range(n)])

    # Cumulative constraints
    for col in range(width):
        sum_h = 0
        for j in range(n):
            if x[j] == col:
                sum_h += h[j]
        opt.add(sum_h < height)

    for row in range(round(h_max)):
        sum_w = 0
        for j in range(n):
            if y[j] == row:
                sum_w += w[j]
        opt.add(sum_w < width)

    # Symmetry breaking constraint - Steinberg
    opt.add([x[max_area_idx] <= 1 + (width - w[max_area_idx]) / 2,
             y[max_area_idx] <= 1 + (height - h[max_area_idx]) / 2])

    t_start = process_time()
    opt.minimize(height)
    check = opt.check()
    model = opt.model()
    delta_t = process_time() - t_start

    if check == sat:
        height = model.evaluate(height)
        chip_x = [model.evaluate(x_i) for x_i in x]
        chip_y = [model.evaluate(y_i) for y_i in y]

        if allow_rotation:
            chip_w = [model.evaluate(w_i) for w_i in w]
            chip_h = [model.evaluate(h_i) for h_i in h]

        print(f'Solution: height = {height} (found in {delta_t:.3f} s)')

        # Write solution to file
        out_filename = f'../{"out_rot" if allow_rotation else "out"}/out-{instance}.txt'
        new_lines = [f'{width} {height}\n', f'{n}\n']
        for w, h, x, y in zip(chip_w, chip_h, chip_x, chip_y):
            new_lines.append(f'{w} {h} {x} {y}\n')

        print(f'Saving at {out_filename}')

        with open(f'{out_filename}', 'w') as file:
            file.writelines(new_lines)

        # Visualize the result
        if visualize:
            visualize_instance(out_filename)

        return height, delta_t
    else:
        print('No solution found within time limit.')
        return 0, delta_t


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", help="number of the instance to run", type=int)
    parser.add_argument("-r", "--allow_rotation", help="allow rotation of chips", action='store_true')
    parser.add_argument("-t", "--timeout", help="timeout to solve the instance", default=5, type=int)
    parser.add_argument("-v", "--visualize", help="visualize the result", action='store_true')
    args = parser.parse_args()

    run_instance(instance=args.instance,
                 allow_rotation=args.allow_rotation,
                 timeout=args.timeout,
                 visualize=args.visualize)
