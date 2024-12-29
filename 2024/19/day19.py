import sys
from typing import Tuple, List, Dict


def load_data(input_path: str) -> Tuple[List[str], List[str]]:
    with open(input_path, "rt") as f:
        patterns = [p.strip() for p in f.readline().split(",")]

        targets = []
        for line in f:
            cleaned = line.strip()
            if cleaned:
                targets.append(cleaned)

    return patterns, targets


def is_possible(patterns: List[str], target: str, cache: Dict[str, bool]) -> bool:
    if not target:
        return True

    previously_cached = cache.get(target)
    if previously_cached is not None:
        return previously_cached

    result = False
    for pattern in patterns:
        if target.startswith(pattern):
            result = is_possible(patterns, target[len(pattern):], cache)
            if result:
                break

    cache[target] = result
    return result


def main(input_path: str):
    patterns, targets = load_data(input_path)

    cache = {}
    possible = 0
    for target in targets:
        if is_possible(patterns, target, cache):
            possible += 1

    print(possible)


if __name__ == "__main__":
    main(sys.argv[1])