import argparse
import datetime

from pprint import pprint
from matplotlib.pyplot import grid

from minizinc import Instance, Model, Solver

from visualize import visualize_instance


def run_instance(instance: int, timeout=5, visualize=True):
    # Read instance data
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

    # Load MiniZinc model from file
    model = Model('./cumulative_global.mzn')
    # Find the MiniZinc solver configuration for Gecode
    gecode = Solver.lookup('gecode')
    # Create an Instance of the model for Gecode
    problem_instance = Instance(gecode, model)

    a = 0
    for i in range(n):
        a += block_height[i] * block_width[i]
    
    min_height = a // width
    max_height = sum(block_height) // (width // max(block_width))

    # Set the variables
    problem_instance['width'] = width
    problem_instance['n'] = n
    problem_instance['W'] = block_width
    problem_instance['H'] = block_height
    problem_instance['min_height'] = min_height
    problem_instance['max_height'] = max_height

    # Solve the instance
    result = problem_instance.solve(timeout=datetime.timedelta(minutes=timeout))
    
    print('\nStatistics:\n')
    print(f'    Solutions : {result.statistics["nSolutions"]}')
    print(f' Num of nodes : {result.statistics["nodes"]}')
    print(f'     Failures : {result.statistics["failures"]}')
    print(f'     Restarts : {result.statistics["restarts"]}')
    print(f'         Time : {result.statistics["solveTime"]}')
    print()

    # Output
    height = result['objective']
    block_x = result['X']
    block_y = result['Y']

    # print(result['index'])
    # print(result['indexx'])
    # print(result['indexy'])
    # print(result['indexxy'])
    
    print('Solution:\n')
    for y in reversed(range(height)):
        for x in range(width):
            print(f'{result["grid2d"][x][y]:2d}', end='')
        print()
    print()

    # print('X reversed\n')
    # for y in reversed(range(height)):
    #     for x in range(width):
    #         print(f'{result["gridx"][x + width * y]:2d}', end='')
    #     print()
    # print()

    # print('Y reversed\n')
    # for y in reversed(range(height)):
    #     for x in range(width):
    #         print(f'{result["gridy"][x + width * y]:2d}', end='')
    #     print()
    # print()

    # print('XY reversed\n')
    # for y in reversed(range(height)):
    #     for x in range(width):
    #         print(f'{result["gridxy"][x + width * y]:2d}', end='')
    #     print()
    # print()

    # Write solution to file
    out_filename = f'../out/out-{instance}.txt'
    new_lines = [f'{width} {height}\n', f'{n}\n']
    for w, h, x, y in zip(block_width, block_height, block_x, block_y):
        new_lines.append(f'{w} {h} {x} {y}\n')

    print(f'Saving at {out_filename}')
    # for line in new_lines: 
    #   print(line, end='')

    with open(f'{out_filename}', 'w') as file: 
        file.writelines(new_lines)

    # Visualize the result
    if visualize: 
        visualize_instance(out_filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="number of the instance to run", required=True, type=int)
    parser.add_argument("-t", "--timeout", help="maximum time allowed to run the istance", default=5, type=int)
    parser.add_argument("-v", "--visualize", help="visualize the result", action='store_true')
    args = parser.parse_args()

    run_instance(args.instance, timeout=args.timeout, visualize=args.visualize)
