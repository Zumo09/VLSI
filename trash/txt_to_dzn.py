import os

directory = '../instances'
data = '../data'

if not os.path.exists(data):
    os.mkdir(data)

for filename in os.listdir(directory):
    print(filename)
    path = os.path.join(directory, filename)
    # Read instance data
    with open(path) as file:
        lines = file.readlines()

    width = int(lines[0])
    n = int(lines[1])
    chip_w = []
    chip_h = []

    for i in range(2, 2 + n):
        w, h = lines[i].split()
        chip_w.append(int(w))
        chip_h.append(int(h))

    new_lines = [
        f'{width=};\n',
        f'{n=};\n',
        f'{chip_w=};\n',
        f'{chip_h=};'
    ]
    print(new_lines)

    path_out = os.path.join(data, filename[:-4]+'.dzn')
    with open(path_out, 'w') as file:
        file.writelines(new_lines)
