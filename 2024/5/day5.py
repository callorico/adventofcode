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

    # Part 1
    # total = 0
    # for u in updates:
    #     valid_update = True
    #     for i in range(len(u)):
    #         current = u[i]
    #         after = set(u[i+1:])

    #         must_be_after_current = constraints[current]
    #         if after.difference(must_be_after_current):
    #             valid_update = False
    #             break
    #     if valid_update:
    #         total += midpoint(u)

    # print(total)

    # Part 2
    total = 0
    for u in updates:
        update_with_key = []
        for i in range(len(u)):
            current = u[i]
            rest = list(u)
            del rest[i]

            must_be_after_current = constraints[current]
            # Count the number of constraint violations for the update value
            # at the current position. The higher the number of violations, the
            # farther to the right the value needs to be pushed. The constraint
            # violation count is effectively the index position within the sorted
            # list.
            position = len(set(rest).difference(must_be_after_current))
            update_with_key.append((current, position))

        sorted_update = [e[0] for e in sorted(update_with_key, key=lambda x: x[1])]
        if sorted_update != u:
            print(f"incorrectly ordered: {u}, sorted: {sorted_update}")
            total += midpoint(sorted_update)

    print(total)


if __name__ == '__main__':
    main(sys.argv[1])




