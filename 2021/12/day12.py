import sys
from typing import List, Tuple, Dict, Set
from collections import defaultdict, Counter


def load_data(input_path: str) -> Dict[str, Set[str]]:
    paths = defaultdict(set)
    with open(input_path, 'r') as f:
        for line in f:
            start, end = line.strip().split('-')
            paths[start].add(end)
            paths[end].add(start)

    return paths


def is_valid_path(path: List[str], next_cave: str) -> bool:
    if not next_cave.islower():
        return True

    counts = Counter()
    for p in path:
        if p.islower():
            counts[p] += 1

    counts[next_cave] += 1

    if counts['start'] > 1:
        return False

    frequencies = counts.most_common(2)
    _, most_common = frequencies[0]
    next_most_visited = 0
    if len(frequencies) > 1:
        _, next_most_visited  = frequencies[1]

    return most_common <=2 and next_most_visited <= 1


def find_all(path: List[str], all_paths: Dict[str, Set[str]]) -> List[List[str]]:
    """Returns all paths that start with the given path prefix"""
    cave = path[-1]

    if cave == 'end':
        return [path]

    next_caves = all_paths[cave]

    paths = [path]
    for next_cave in next_caves:
        if next_cave.islower():
            if not is_valid_path(path, next_cave):
                continue

        for p in find_all(path + [next_cave], all_paths):
            paths.append(p)

    return paths


def part2(input_path: str):
    caves = load_data(input_path)
    print(caves)

    all_paths = find_all(['start'], caves)
    # for path in all_paths:
    #     print(path)

    paths_with_end = [p for p in all_paths if p[-1] == 'end']
    for path in paths_with_end:
        print(path)

    print(len(paths_with_end))

# def find_all(path: List[str], all_paths: Dict[str, Set[str]]) -> List[List[str]]:
#     """Returns all paths that start with the given path prefix"""
#     cave = path[-1]

#     if cave == 'end':
#         return [path]

#     next_caves = all_paths[cave]

#     paths = [path]
#     for next_cave in next_caves:
#         if next_cave.islower():
#             if next_cave in path:
#                 continue

#         for p in find_all(path + [next_cave], all_paths):
#             paths.append(p)

#     return paths


def part1(input_path: str):
    caves = load_data(input_path)
    print(caves)

    all_paths = find_all(['start'], caves)
    # for path in all_paths:
    #     print(path)

    paths_with_end = [p for p in all_paths if p[-1] == 'end']
    for path in paths_with_end:
        print(path)

    print(len(paths_with_end))


if __name__ == '__main__':
    part2(sys.argv[1])