import os

for filename in os.listdir('instances'):
    with open(f'instances/{filename}', 'r') as file:
        lines = file.readlines()

    new_lines = [f'width={int(lines[0])};\n']

    n = int(lines[1])
    new_lines.append(f'n={n};\n')

    new_lines.append(f'blocks=array2d(1..{n}, 1..2, [\n')

    for i in range(2, 2+n):
        w, h = lines[i].split()
        new_lines.append(f'\t{w}, {h},\n')

    new_lines.append(']);')

    with open(f'cp/data/{filename[:-4]}.dnz', 'w') as file:
        file.writelines(new_lines)