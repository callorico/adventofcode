import sys
from typing import Tuple


Area = Tuple[Tuple[int, int], Tuple[int, int]]

def load_data(input_path: str):
    def parse_range(range: str) -> Area:
        return tuple(int(c) for c in range.split('..'))

    with open(input_path, 'r') as f:
        ranges = f.read().strip().split(':')[1].strip()
        xrange, yrange = ranges.split(', ')

        return (
            parse_range(xrange.split('=')[1]),
            parse_range(yrange.split('=')[1])
        )


def launch(velocity: Tuple[int, int], target: Area) -> Tuple[int, bool]:
    # print(f'Testing launch velocity of {velocity}')
    step = 0
    x = 0
    y = 0
    max_y = 0
    x_velocity, y_velocity = velocity
    x_bounds, y_bounds = target

    while True:
        x += x_velocity
        y += y_velocity

        # print(f'Step: {step}, pos: {x},{y}')
        if y > max_y:
            max_y = y

        if x > x_bounds[1] or y < y_bounds[0]:
            # We've fallen under the target or shot past it. We can never
            # recover at this point.
            inside = False
            break

        if x >= x_bounds[0] and x <= x_bounds[1] and y >= y_bounds[0] and y <= y_bounds[1]:
            inside = True
            break

        if x_velocity > 0:
            x_velocity -= 1
        elif x_velocity < 0:
            x_velocity += 1
        y_velocity -= 1

        step += 1

    return max_y, inside

def part2(input_path: str):
    target_area = load_data(input_path)

    xrange, yrange = target_area

    possible = []
    for x in range(xrange[1] + 1):
        for y in range(yrange[0], 500):
            _, inside = launch((x, y), target_area)
            if inside:
                possible.append((x, y))

    print(len(possible))

def part1(input_path: str):
    target_area = load_data(input_path)
    print(target_area)

    xrange, yrange = target_area
    min_x = xrange[0]

    # What is the smallest x velocity that hits the target
    x_velocity = 0
    step = 0
    while x_velocity < min_x:
        step += 1
        x_velocity += step

    max_height = 0
    for y_velocity in range(500, 0, -1):
        print(f'Testing {step}, {y_velocity}')
        height, inside = launch((step, y_velocity), target_area)
        if inside:
            if height > max_height:
                max_height = height
                break

    print(f'Max height: {max_height} at {step}, {y_velocity}')


if __name__ == '__main__':
    part2(sys.argv[1])