import sys
import re
from dataclasses import dataclass
from typing import Tuple, List
from collections import Counter


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


def quadrants(robots: List[Robot], max_x: int, max_y: int) -> Tuple[int, int, int, int]:
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

    return (ul, ur, ll, lr)


def asymmetry(robots: List[Robot], max_x: int, max_y: int) -> int:
    position = Counter()
    for r in robots:
        position[r.position] += 1

    asymmetry = 0
    half_width = max_x // 2

    for pos, count in position.items():
        distance = half_width - pos[0]

        mirrored_pos = (half_width + distance, pos[1])
        if mirrored_pos not in position:
            asymmetry += count

    return asymmetry



def main(input_path: str):
    robots = load_data(input_path)
    # print(robots)

    # Part 1
    max_x = 101
    max_y = 103
    # max_x = 11
    # max_y = 7

    # Every robot covers every cell in the grid in 10403s. Calculated with:
    # for r in robots:
    #     positions = {r.position: 0}
    #     seconds = 0
    #     while True:
    #         r.move(1, max_x, max_y)
    #         seconds += 1
    #         prev_seconds = positions.get(r.position)
    #         if prev_seconds is not None:
    #             print(f"cycled back to same position from {prev_seconds}")
    #             break
    #         positions[r.position] = seconds

    #     print(f"{r}: {len(positions)} after {seconds}s")
    # print(len(positions))


    # print("Start")
    # # print_grid(robots, max_x, max_y)

    min_asymmetry = None
    best_seconds = 0
    seconds = 0
    while seconds < 10403:
        for r in robots:
            r.move(1, max_x, max_y)
        seconds += 1

        target = asymmetry(robots, max_x, max_y)
        if min_asymmetry is None or target < min_asymmetry:
            min_asymmetry = target
            best_seconds = seconds

    print(f"Min asymmetry was: {min_asymmetry} at {best_seconds}")

    # Robots are all back in their starting positions again
    for r in robots:
        r.move(best_seconds, max_x, max_y)

    print_grid(robots, max_x, max_y)

    # Part 1
    # for r in robots:
    #     r.move(100, max_x, max_y)
    # ul, ur, ll, lr = quadrants(robots, max_x, max_y)
    # safety_factor = ul * ur * ll * lr
    # print(safety_factor)


if __name__ == "__main__":
    main(sys.argv[1])