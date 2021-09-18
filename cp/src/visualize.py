import argparse
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle


def visualize_instance(filename):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    _, ax = plt.subplots()

    w, h = lines[0].split()
    w, h = int(w), int(h)
    n = int(lines[1])

    ax.set_title(f'{filename} (h = {h})')
    ax.set_xticks(range(w+1))
    ax.set_yticks(range(h+1))
    ax.axis('equal')
    ax.grid(True)
    ax.plot([0, w], [0, 0], c='k')
    ax.plot([0, w], [h, h], c='k')
    ax.plot([0, 0], [0, h], c='k')
    ax.plot([w, w], [0, h], c='k')
    
    for i in range(2, 2 + n):
        w, h, x, y = lines[i].split()
        w, h, x, y = int(w), int(h), int(x), int(y)
        ax.add_patch(Rectangle((x, y), w, h, color=colors[i % 6], alpha=0.2))
        ax.add_patch(Rectangle((x, y), w, h, fill=None, edgecolor='black'))
        ax.text(x+0.1, y+0.1, f'{w}x{h}')

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="number of the instance to visualize", required=True, type=int)
    args = parser.parse_args()

    visualize_instance(f'../out/out-{args.instance}.txt')
