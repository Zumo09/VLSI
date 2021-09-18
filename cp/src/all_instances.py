import os
import argparse

from visualize import visualize_instance
from run import run_instance

def run_all(timeout):
    for i in range(1, 41):
        print('\n\nIntsance', i)
        try:
            run_instance(i, timeout=timeout, visualize=False)
        except KeyboardInterrupt:
            print('\n\nExit')

def visualize_all():
    path = '../out'
    files = os.listdir(path)

    for i in range(1, 41):
        filename = f'out-{i}.txt'
        if filename in files:
            visualize_instance(f'{path}/{filename}')


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-r", "--run_all", help="run all the instances", action='store_true')
    parser.add_argument("-t", "--timeout", help="timeout for each instance", default=5)
    parser.add_argument("-v", "--visualize_all", help="visualize all the instances", action='store_true')
    args = parser.parse_args()

    if args.run_all:
        run_all(args.timeout)
    else:
        print('Using previous run')
    
    if args.visualize_all:
        visualize_all()
    else:
        print('No visualization')