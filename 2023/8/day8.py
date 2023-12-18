import sys
from itertools import cycle
from typing import Tuple


def load_data(input_path) -> Tuple[str, dict[str, Tuple[str, str]]]:
    nodes: dict[str, Tuple[str, str]] = {}

    with open(input_path, "r") as f:
        instructions = f.readline().strip()
        f.readline()

        for line in f:
            label, paths = line.strip().split(" = ")
            left, right = paths.strip("()").split(", ")
            nodes[label] = (left, right)


    return instructions, nodes


def main(input_path):
    instructions, nodes = load_data(input_path)
    print(instructions) 
    print(nodes)

    current = "AAA"
    steps = 0
    moves = cycle(instructions)
    while current != "ZZZ":
        move = next(moves)
        if move == "L":
            index = 0
        elif move == "R":
            index = 1
        else:
            raise ValueError(f"Unknown move: {move}")

        current = nodes[current][index]
        steps += 1

    print(f"Took {steps} steps to reach desired state")


if __name__ == "__main__":
    main(sys.argv[1])