import argparse
import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle


def visualize_instance_symmetry(filename):
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    
    with open(filename, 'r') as file:
        lines = file.readlines()
    _, ((ax, axx), (axy, axxy)) = plt.subplots(2, 2)

    width, height = lines[0].split()
    width, height = int(width), int(height)
    n = int(lines[1])

    ax.set_title(f'{filename} (height = {height})')
    ax.set_xticks(range(width+1))
    ax.set_yticks(range(height+1))
    ax.axis('equal')
    ax.grid(True)
    ax.plot([0, width], [0, 0], c='k')
    ax.plot([0, width], [height, height], c='k')
    ax.plot([0, 0], [0, height], c='k')
    ax.plot([width, width], [0, height], c='k')

    axx.set_title(f'{filename} (height = {height})')
    axx.set_xticks(range(width+1))
    axx.set_yticks(range(height+1))
    axx.axis('equal')
    axx.grid(True)
    axx.plot([0, width], [0, 0], c='k')
    axx.plot([0, width], [height, height], c='k')
    axx.plot([0, 0], [0, height], c='k')
    axx.plot([width, width], [0, height], c='k')

    axy.set_title(f'{filename} (height = {height})')
    axy.set_xticks(range(width+1))
    axy.set_yticks(range(height+1))
    axy.axis('equal')
    axy.grid(True)
    axy.plot([0, width], [0, 0], c='k')
    axy.plot([0, width], [height, height], c='k')
    axy.plot([0, 0], [0, height], c='k')
    axy.plot([width, width], [0, height], c='k')

    axxy.set_title(f'{filename} (height = {height})')
    axxy.set_xticks(range(width+1))
    axxy.set_yticks(range(height+1))
    axxy.axis('equal')
    axxy.grid(True)
    axxy.plot([0, width], [0, 0], c='k')
    axxy.plot([0, width], [height, height], c='k')
    axxy.plot([0, 0], [0, height], c='k')
    axxy.plot([width, width], [0, height], c='k')
    
    for i in range(2, 2 + n):
        w, h, x, y = lines[i].split()
        w, h, x, y = int(w), int(h), int(x), int(y)

        xx = width - x - w
        yy = height - y - h

        ax.add_patch(Rectangle((x, y), w, h, color=colors[i % 6], alpha=0.2))
        ax.add_patch(Rectangle((x, y), w, h, fill=None, edgecolor='black'))
        ax.text(x+0.1, y+0.1, f'{w}x{h}')

        axx.add_patch(Rectangle((xx, y), w, h, color=colors[i % 6], alpha=0.2))
        axx.add_patch(Rectangle((xx, y), w, h, fill=None, edgecolor='black'))
        axx.text(xx+0.1, y+0.1, f'{w}x{h}')

        axy.add_patch(Rectangle((x, yy), w, h, color=colors[i % 6], alpha=0.2))
        axy.add_patch(Rectangle((x, yy), w, h, fill=None, edgecolor='black'))
        axy.text(x+0.1, yy+0.1, f'{w}x{h}')

        axxy.add_patch(Rectangle((xx, yy), w, h, color=colors[i % 6], alpha=0.2))
        axxy.add_patch(Rectangle((xx, yy), w, h, fill=None, edgecolor='black'))
        axxy.text(xx+0.1, yy+0.1, f'{w}x{h}')

    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instance", help="number of the instance to visualize", required=True, type=int)
    args = parser.parse_args()

    visualize_instance_symmetry(f'../cp/out/out-{args.instance}.txt')