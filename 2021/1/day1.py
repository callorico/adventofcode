import sys
import itertools

def load_data(input_path):
    with open(input_path, 'r') as f:
        return [int(line) for line in f]


def window(index, readings):
    return readings[index] + readings[index + 1] + readings[index + 2]


def main(input_path):
    readings = load_data(input_path)
    increased = 0
    for index, reading in enumerate(readings):
        if index >= 1 and readings[index - 1] < reading:
            increased += 1

    print(f'Increases: {increased}')

    increased = 0
    for index in range(0, len(readings) - 3):
        if window(index, readings) < window(index + 1, readings):
            increased += 1

    print(f'Window increases: {increased}')



if __name__ == '__main__':
    main(sys.argv[1])
