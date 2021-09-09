import argparse
import datetime

from minizinc import Instance, Model, Solver

from visualize import visualize_instance


def run_instance(instance: int, timeout=5, visualize=True):
    with open(f'../instances/ins-{instance}.txt', 'r') as file:
        lines = file.readlines()

    width = int(lines[0])
    n = int(lines[1])

    block_width = []
    block_height = []

    for i in range(2, 2+n):
        w, h = lines[i].split()
        block_width.append(int(w))
        block_height.append(int(h))

    # Load model from file
    model = Model('./cumulative_global.mzn')
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup('gecode')
    # Create an Instance of the model for Gecode
    problem_instance = Instance(gecode, model)

    problem_instance['width'] = width
    problem_instance['n'] = n
    problem_instance['W'] = block_width
    problem_instance['H'] = block_height

    result = problem_instance.solve(timeout=datetime.timedelta(minutes=timeout))

    # Output
    height = result['objective']
    block_x = result['X']
    block_y = result['Y']

    out_filename = f'../out/out-{instance}.txt'

    new_lines = [f'{width} {height}\n', f'{n}\n']

    for w, h, x, y in zip(block_width, block_height, block_x, block_y):
        new_lines.append(f'{w} {h} {x} {y}\n')

    print(f'Saving at {out_filename}')
    for line in new_lines:
        print(line, end='')

    with open(f'{out_filename}', 'w') as file:
        file.writelines(new_lines)

    if visualize:
        visualize_instance(out_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="number of the instance to run", required=True, type=int)
    parser.add_argument("-t", "--timeout", help="maximum time allowed to run the istance", type=int)
    parser.add_argument("-v", "--visualize", help="visualize the result", action='store_true')
    args = parser.parse_args()

    run_instance(args.instance, timeout=args.timeout, visualize=args.visualize)
