from visualize import visualize_instance


def visualize_solution(use_chuffed, allow_rotation, instance):
    dir_name = f'out_{"chuffed" if use_chuffed else "gecode"}{"_rot" if allow_rotation else ""}'
    filename = f'../{dir_name}/out-{instance}.txt'
    try:
        visualize_instance(filename)
    except FileNotFoundError:
        print('No solution for instance', filename)


def main():
    for instance in range(10, 41):
        for chu in [False, True]:
            for rot in [False, True]:
                visualize_solution(chu, rot, instance)


if __name__ == "__main__":
    main()
