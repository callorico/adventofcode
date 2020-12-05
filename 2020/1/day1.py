import sys
import itertools
def load_data(input_path):
    with open(input_path, 'r') as f:
        return [int(line) for line in f]

def find_pair(numbers, desired_sum):
    # O(n)
    desired_targets = set()
    for n in numbers:
        target = desired_sum - n
        if target in desired_targets:
            return n, target
        desired_targets.add(n)

def find_triplet(numbers):
    # O(n^2)
    for i, n in enumerate(numbers):
        target = 2020 - n
        numbers_copy = numbers[:i] + numbers[i + 1:]
        match = find_pair(numbers_copy, target)
        if match:
            return n, match[0], match[1]

def brute_triplet(numbers):
    for n1, n2, n3 in itertools.combinations(numbers, 3):
        if n1 + n2 + n3 == 2020:
            return n1, n2, n3

def main(input_path):
    numbers = load_data(input_path)
    print(numbers)

    # n1, n2, n3 = brute_triplet(numbers)
    # print(n1, n2, n3)
    # print(n1 + n2 + n3)
    # print(n1 * n2 * n3)
    # n1, n2 = find_pair(numbers, 2020)
    # print(n1, n2)
    # print(n1 + n2)
    # print(n1 * n2)
    n1, n2, n3 = find_triplet(numbers)
    print(n1, n2, n3)
    print(n1 + n2 + n3)
    print(n1 * n2 * n3)


if __name__ == '__main__':
    main(sys.argv[1])