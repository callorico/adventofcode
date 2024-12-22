import sys
import re
from dataclasses import dataclass
from typing import Tuple, List


@dataclass
class Robot:
    position: Tuple[int, int]
    velocity: Tuple[int, int]

    def move(self, seconds: int, max_x: int, max_y: int):
        delta_x = self.velocity[0] * seconds
        delta_y = self.velocity[1] * seconds

        # Calculate new position considering wrap
        x = (self.position[0] + delta_x) % max_x
        y = (self.position[1] + delta_y) % max_y

        self.position = (x, y)


def load_data(input_path: str) -> List[Robot]:
    robots = []
    with open(input_path, "rt") as f:
        for line in f:
            coordinates = re.findall(r"(-?\d+),(-?\d+)", line)
            if coordinates:
                print(coordinates)
                p, v = coordinates
                robots.append(
                    Robot(
                        position=tuple([int(n) for n in p]),
                        velocity=tuple([int(n) for n in v])
                    )
                )

    return robots


def print_grid(robots: List[Robot], max_x: int, max_y: int):
    for y in range(max_y):
        for x in range(max_x):
            total = 0
            for r in robots:
                if r.position == (x, y):
                    total += 1
            if total:
                print(f"{total}", end="")
            else:
                print(".", end="")
        print()

def main(input_path: str):
    robots = load_data(input_path)
    print(robots)

    # Part 1
    max_x = 101
    max_y = 103
    # max_x = 11
    # max_y = 7

    print("Start")
    print_grid(robots, max_x, max_y)

    for r in robots:
        r.move(100, max_x, max_y)

    print("End")
    print_grid(robots, max_x, max_y)

    # Count robots in each quadrant

    half_width = max_x // 2
    half_height = max_y // 2

    ul = ur = ll = lr = 0

    for r in robots:
        if r.position[0] < half_width:
            if r.position[1] < half_height:
                ul += 1
            elif r.position[1] > half_height:
                ll += 1
        elif r.position[0] > half_width:
            if r.position[1] < half_height:
                ur += 1
            elif r.position[1] > half_height:
                lr += 1

    safety_factor = ul * ur * ll * lr
    print(safety_factor)


if __name__ == "__main__":
    main(sys.argv[1])