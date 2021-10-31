from typing import AnyStr, Union

from pandas._typing import FilePathOrBuffer

from run import run_instance
import pandas as pd

allow_rotation = True

print(f'ROTATION {"" if allow_rotation else "NOT "}ALLOWED')
df = pd.DataFrame(columns=['Instance', 'Height', 'Time'])
for instance in range(1, 41):
    times = []
    for i in range(5):
        height, delta_t = run_instance(instance=instance,
                                       allow_rotation=allow_rotation,
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

path: Union[FilePathOrBuffer[AnyStr], None] = f'../csv/out{"_rotation" if allow_rotation else  ""}.csv'
df.to_csv(path, sep=';')
