import os

from run import run_instance
import pandas as pd
import datetime

allow_rotation = True
use_chuffed = False
start = 11
end = 40

path = f'../csv/{"chuffed" if use_chuffed else "gecode"}{"_rotation" if allow_rotation else  ""}.csv'

if os.path.isfile(path):
    df = pd.read_csv(path, index_col=0)
else:
    df = pd.DataFrame(columns=['Instance', 'Height', 'Time'])

print(f'ROTATION {"" if allow_rotation else "NOT "}ALLOWED')
print(f'{"CHUFFED" if use_chuffed else "GECODE"} SOLVER')
for instance in range(start, end + 1):
    times = []
    for i in range(5):
        print(datetime.datetime.now())
        height, delta_t = run_instance(instance=instance,
                                       allow_rotation=allow_rotation,
                                       use_chuffed=use_chuffed,
                                       timeout=5,
                                       visualize=False)

        df = df.append({'Instance': instance, 'Run': i, 'Height': height, 'Time': delta_t}, ignore_index=True)

        times.append(delta_t)
        if delta_t > 299:
            print(f'Timeout reached for instance {instance}, run {i}. Skipping')
            break
        elif delta_t > 200:
            print(f'Timeout not reached but too much time. Skipping')
            break

    mean = sum(times)/len(times)
    print(f'\n\nInstance {instance}: time = {mean}\n\n\n')
    df = df.append({'Instance': instance, 'Run': None, 'Height': None, 'Time': mean}, ignore_index=True)

    df.to_csv(path)
