import argparse

from minizinc import Instance, Model, Solver

from visualize import visualize_instance


def run_instance(inst: int, visualize=True):
    with open(f'../../instances/ins-{inst}.txt', 'r') as file:
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
    instance = Instance(gecode, model)

    instance['width'] = width
    instance['n'] = n
    instance['W'] = block_width
    instance['H'] = block_height

    result = instance.solve()

    # Output
    height = result['objective']
    block_x = result['X']
    block_y = result['Y']

    out_filename = f'../out/out-{inst}.txt'

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
    parser.add_argument("-i", "--instance", help="number of the instance to run", default=1, type=int)
    parser.add_argument("--visualize", help="visualize the result", action='store_true')
    args = parser.parse_args()

    run_instance(args.instance, visualize=args.visualize)
