import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def visualize_instance(filename, show=True):
    _, ax = plt.subplots()
    ax.axis('equal')

    with open(filename, 'r') as file:
        lines = file.readlines()

    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    w, h = lines[0].split()

    w, h = int(w), int(h)

    ax.set_title(f'{filename} (h = {h})')
    ax.set_xticks(range(w+1))
    ax.set_yticks(range(h+1))
    ax.grid(True)


    ax.plot([0, w], [0, 0], c='k')
    ax.plot([0, w], [h, h], c='k')
    ax.plot([0, 0], [0, h], c='k')
    ax.plot([w, w], [0, h], c='k')
    n = int(lines[1])
    for i in range(2, 2 + n):
        w, h, x, y = lines[i].split()
        w, h, x, y = int(w), int(h), int(x), int(y)
        ax.add_patch(Rectangle((x, y), w, h, color=colors[i % 6], alpha=0.2))
        ax.add_patch(Rectangle((x, y), w, h, fill=None, edgecolor='black'))
        ax.text(x, y, f'{w}x{h}')
        # ax.add_patch(Rectangle((x, y), w, h, fill=None, edgecolor=colors[i % 6]))

    if show:
        plt.show()
