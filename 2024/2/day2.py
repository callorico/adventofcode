import sys
from typing import Dict, Tuple, List
from collections import Counter

def load_data(input_path: str) -> List[List[int]]:
    reports: List[int] = []

    with open(input_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue

            levels = [int(t) for t in stripped.split(" ")]
            reports.append(levels)
    return reports


def is_safe(levels: List[int]) -> bool:
    prev = levels[0]
    prev_diff = 0
    for level in levels[1:]:
        diff = prev - level
        if diff == 0:
            return False
        elif diff > 0 and prev_diff < 0:
            return False
        elif diff < 0 and prev_diff > 0:
            return False


        step_change = abs(diff)
        if step_change < 1 or step_change > 3:
            return False

        prev = level
        prev_diff = diff

    return True


def main(input_path):
    reports = load_data(input_path)

    # Part 1
    #total_safe = sum(is_safe(levels) for levels in reports)
    #print(total_safe)

    # Part 2: The grossest solution possible
    total_safe = 0
    for levels in reports:
        if is_safe(levels):
            total_safe += 1
        else:
            for i in range(len(levels)):
                potential_levels = list(levels)
                del potential_levels[i]
                if is_safe(potential_levels):
                    total_safe += 1
                    break

    print(total_safe)



if __name__ == '__main__':
    main(sys.argv[1])

