import pandas as pd

from run import run_instance

allow_rotation = False
use_chuffed = True

path = f'../csv/{"chuffed" if use_chuffed else "gecode"}{"_rotation" if allow_rotation else  ""}.csv'

print(f'ROTATION {"" if allow_rotation else "NOT "}ALLOWED')
print(f'{"CHUFFED" if use_chuffed else "GECODE"} SOLVER')
df = pd.DataFrame(columns=['Instance', 'Height', 'Time'])
for instance in range(1, 41):
    times = []
    for i in range(5):
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

    mean = sum(times)/len(times)
    print(f'\n\nInstance {instance}: time = {mean}\n\n\n')
    df = df.append({'Instance': instance, 'Run': None, 'Height': None, 'Time': mean}, ignore_index=True)

    df.to_csv(path)
