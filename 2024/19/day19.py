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


def pattern_counts(patterns: List[str], target: str, cache: Dict[str, int]) -> int:
    if not target:
        return 0

    previously_cached = cache.get(target)
    if previously_cached is not None:
        return previously_cached

    matches = 0
    for pattern in patterns:
        if target.startswith(pattern):
            remaining_target = target[len(pattern):]
            if not remaining_target:
                matches += 1
            else:
                matches += pattern_counts(patterns, remaining_target, cache)

    # print(f"{target} has {matches} matches.")
    cache[target] = matches
    return matches


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
    print(patterns)

    # is_possible_cache = {}
    # candidates = []
    # for target in targets:
    #     if is_possible(patterns, target, is_possible_cache):
    #         candidates.append(target)

    cache = {}
    total_patterns = 0
    for target in targets:
        # print(f"--- Evaluating {target} ---")
        count = pattern_counts(patterns, target, cache)
        print(f"{target} has {count} possible arrangements.")
        total_patterns += count

    print(total_patterns)


if __name__ == "__main__":
    main(sys.argv[1])