import argparse
import datetime

from minizinc import Instance, Model, Solver

from visualize import visualize_instance


def run_instance(instance: int, allow_rotation=False, use_chuffed=False, timeout=5, visualize=True):
    # Read instance data
    with open(f'../instances/ins-{instance}.txt', 'r') as file:
        lines = file.readlines()

    width = int(lines[0])
    n = int(lines[1])
    chip_w = []
    chip_h = []

    for i in range(2, 2+n):
        w, h = lines[i].split()
        chip_w.append(int(w))
        chip_h.append(int(h))

    # Load MiniZinc model from file
    if allow_rotation:
        model = Model('./model_rotation.mzn')
    else:
        model = Model('./model.mzn')

    # Find the MiniZinc solver configuration
    if use_chuffed:
        solver = Solver.lookup('chuffed')
    else:
        solver = Solver.lookup('gecode')

    # Create an Instance of the model for Gecode
    problem_instance = Instance(solver, model)

    # Set the variables
    problem_instance['width'] = width
    problem_instance['n'] = n
    problem_instance['chip_w'] = chip_w
    problem_instance['chip_h'] = chip_h

    print(f'Running instance {instance}{" with rotation allowed " if allow_rotation else " "}'
          f'using {"chuffed" if use_chuffed else "gecode"} solver (timeout {timeout} min)')
    # Solve the instance
    result = problem_instance.solve(timeout=datetime.timedelta(minutes=timeout))

    # Output
    try:
        height = result['height']
        chip_x = result['x']
        chip_y = result['y']

        delta_t = result.statistics["solveTime"].total_seconds()
    except KeyError:
        print('No solution found within time limit.')
        return 0, timeout*60

    print(f'Solution: height = {height} (found in {delta_t:.3f} s)')

    if allow_rotation:
        r = result['r']
        for i in range(n):
            if r[i]:
                chip_h[i], chip_w[i] = chip_w[i], chip_h[i]

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


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("instance", help="number of the instance to run", type=int)
    parser.add_argument("-r", "--allow_rotation", help="allow rotation of chips", action='store_true')
    parser.add_argument("-c", "--use_chuffed", help="use chuffed solver", action='store_true')
    parser.add_argument("-t", "--timeout", help="timeout to solve the instance", default=5, type=int)
    parser.add_argument("-v", "--visualize", help="visualize the result", action='store_true')
    args = parser.parse_args()

    run_instance(instance=args.instance,
                 allow_rotation=args.allow_rotation,
                 use_chuffed=args.use_chuffed,
                 timeout=args.timeout,
                 visualize=args.visualize)
