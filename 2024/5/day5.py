import sys
import re
from typing import List, Tuple, Dict, Set
from collections import defaultdict


def load_data(input_path: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    with open(input_path, 'rt') as f:
        orderings = []
        for line in f:
            if not line.strip():
                break

            page1, page2 = line.split("|", 1)
            orderings.append((int(page1), int(page2)))

        updates = []
        for line in f:
            if not line.strip():
                break

            updates.append([int(p) for p in line.split(",")])

    return orderings, updates



def midpoint(update: List[int]) -> int:
    return update[len(update) // 2]


def main(input_path):
    orderings, updates = load_data(input_path)

    constraints: Dict[int, Set[int]] = defaultdict(set)

    for x, y in orderings:
        constraints[x].add(y)

    total = 0
    for u in updates:
        valid_update = True
        for i in range(len(u)):
            current = u[i]
            after = set(u[i+1:])

            must_be_after_current = constraints[current]
            if after.difference(must_be_after_current):
                valid_update = False
                break

        if valid_update:
            total += midpoint(u)

    print(total)


if __name__ == '__main__':
    main(sys.argv[1])




