import sys
from itertools import cycle
from typing import Tuple
from functools import reduce
import operator
import math


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


def move_until_terminal(start: str, instructions: str, nodes: dict[str, Tuple[str, str]]) -> int:
    current: str = start
    steps = 0
    moves = cycle(instructions)

    terminal_dist: dict[str, Tuple[str, int]] = {}

    while True:
        move = next(moves)
        if move == "L":
            index = 0
        elif move == "R":
            index = 1
        else:
            raise ValueError(f"Unknown move: {move}")

        current = nodes[current][index]
        steps += 1

        if current.endswith("Z"):
            terminal_dist[start] = (current, steps)
            if current in terminal_dist:
                break

            steps = 0
            start = current

    return terminal_dist


def main(input_path):
    instructions, nodes = load_data(input_path)

    current = [s for s in nodes.keys() if s.endswith("A")]
    print(f"starting states: {current}")

    factors = []
    for c in current:
        factors.append(move_until_terminal(c, instructions, nodes))

    print(factors)

    # Conveniently, each starting state has just 1 associated
    # terminal state and it takes the same number of steps
    # to reach that terminal state each time. 
    # 
    # Here we just take the # of steps to the terminal states
    # for each start state.
    steps = [list(f.values())[0][1] for f in factors]
    gcd = math.gcd(*steps)
    steps = reduce(operator.mul, [s // gcd for s in steps]) * gcd
    print(steps)


if __name__ == "__main__":
    main(sys.argv[1])