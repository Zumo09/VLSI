import os
import shutil

chuffed_wins = 0
gecode_wins = 0
tie = 0
none_wins = 0

# g_dir = '../out_gecode_rot'
# c_dir = '../out_chuffed_rot'
# o_dir = '../out_rot'

g_dir = '../out_gecode'
c_dir = '../out_chuffed'
o_dir = '../out'

wcs = 10000

for instance in range(1, 41):
    fname = f'/out-{instance}.txt'

    gecode = wcs
    if os.path.isfile(g_dir + fname):
        with open(g_dir + fname, 'r') as file:
            gecode = int(file.readlines()[0].split()[1])

    chuffed = wcs
    if os.path.isfile(c_dir + fname):
        with open(c_dir + fname, 'r') as file:
            chuffed = int(file.readlines()[0].split()[1])

    if gecode == wcs and chuffed == wcs:
        print(f'{instance = }\tNone wins')
        none_wins += 1
        continue

    if chuffed == gecode:
        print(f'{instance = }\tTie          ({chuffed})')
        tie += 1
        shutil.copy(c_dir + fname, o_dir + fname)
        continue

    if chuffed < gecode:
        print(f'{instance = }\tChuffed wins ({chuffed})')
        chuffed_wins += 1
        shutil.copy(c_dir + fname, o_dir + fname)
        continue

    if gecode < chuffed:
        print(f'{instance = }\tGecode wins  ({gecode})')
        gecode_wins += 1
        shutil.copy(g_dir + fname, o_dir + fname)
        continue

print()
print(f'{none_wins=}')
print(f'{tie=}')
print(f'{chuffed_wins=}')
print(f'{gecode_wins=}')