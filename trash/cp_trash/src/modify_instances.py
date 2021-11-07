# This script read the instance file 'ins-i.txt' and
# creates a new txt file named 'ins_i.txt' that can be copy in a .dzn file
# and used as data file in MiniZinc
# instances_path has must be a folder containing the instances file
# in the format described by the pdf project.

txt = [f'../instances/ins-{i}.txt' for i in range(1, 41)]
ins_list = [f'data/ins-{i}.dzn' for i in range(1, 41)]

for i in range(len(txt)):
    with open(txt[i]) as data:
        plaintext = data.readlines()

    s = []
    for j in range(len(plaintext)):
        s.append(plaintext[j].replace('\n', ' '))

    f = open(ins_list[i], 'w')
    f.writelines('W=' + s[0] + ';\n')
    f.writelines('n=' + s[1] + ';\n')
    s[2].replace(' ', ',')
    f.writelines('dimensions=[|' + s[2].replace(' ', ',') + '\n')

    for j in range(3, len(plaintext) - 1):
        f.writelines('|' + s[j].replace(' ', ',') + '\n')

    f.writelines('|' + s[len(plaintext) - 1].replace(' ', ',') + '|]\n')
    f.close()
