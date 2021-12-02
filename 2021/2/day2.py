import sys

def load_data(input_path):
    with open(input_path, 'r') as f:
        for line in f:
            direction, amount = line.split(' ')
            yield direction, int(amount)


def main(input_path):
    directions = list(load_data(input_path))
    horizontal = 0
    depth = 0
    aim = 0
    for direction, step in directions:
        if direction == 'forward':
            horizontal += step
            depth += aim * step
        elif direction == 'up':
            aim -= step
        elif direction == 'down':
            aim += step

    product = horizontal * depth
    print(f'H: {horizontal}, D: {depth}, Product: {product}')

    # Part 1
    # for direction, step in directions:
    #     if direction == 'forward':
    #         horizontal += step
    #     elif direction == 'up':
    #         depth -= step
    #     elif direction == 'down':
    #         depth += step

    # product = horizontal * depth
    # print(f'H: {horizontal}, D: {depth}, Product: {product}')

if __name__ == '__main__':
    main(sys.argv[1])