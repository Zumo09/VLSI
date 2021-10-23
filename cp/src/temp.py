from run import run_instance
import pandas as pd

allow_rotation = False
use_chuffed = False

print(f'ROTATION {"" if allow_rotation else "NOT "}ALLOWED')
print(f'{"CHUFFED" if use_chuffed else "GECODE"} SOLVER')
df = pd.DataFrame(columns=['Instance', 'Height', 'Time'])
for instance in range(1, 41):
    for i in range(5):
        height, delta_t = run_instance(instance=instance,
                                       allow_rotation=allow_rotation,
                                       use_chuffed=use_chuffed,
                                       timeout=5,
                                       visualize=False)

        df = df.append({'Instance': instance, 'Run': i, 'Height': height, 'Time': delta_t}, ignore_index=True)

path = f'../csv/{"chuffed" if use_chuffed else "gecode"}{"_rotation" if allow_rotation else  ""}.csv'
df.to_csv(path, sep=';')