import os

from visualize import visualize_instance
from run import run_instance
from matplotlib.pyplot import show

def run_all():
    ok = True
    i = 1
    ok = input('Run All? Enter to Exit, any key to continue')
    while i <= 40:
        run_instance(i, timeout=1, visualize=False)
        i += 1

def visualize_all():
    path = '../out'
    for filename in os.listdir(path):
        visualize_instance(f'{path}/{filename}', show=False)
    show()


if __name__=='__main__':
    run_all()
    visualize_all()