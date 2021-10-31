import os
import argparse

from visualize import visualize_instance
from run import run_instance


def run_all(last, timeout):
    for i in range(1, last + 1):
        print('\n\nInstance', i)
        run_instance(i, timeout=timeout, visualize=False)


def visualize_all():
    path = '../cp/out_gecode'
    files = os.listdir(path)

    for i in range(1, 41):
        filename = f'out_gecode-{i}.txt'
        if filename in files:
            visualize_instance(f'{path}/{filename}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--last", help="run all the instances until 'last'", default=0, type=int)
    parser.add_argument("-t", "--timeout", help="timeout for each instance", default=5, type=int)
    parser.add_argument("-v", "--visualize_all", help="visualize all the instances", action='store_true')
    args = parser.parse_args()

    if args.last > 0:
        run_all(args.last, args.timeout)
    else:
        print('Using previous run')

    if args.visualize_all:
        visualize_all()
    else:
        print('No visualization')
