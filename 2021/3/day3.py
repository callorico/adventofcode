import sys
from collections import Counter


def load_data(input_path):
    with open(input_path, 'r') as f:
        for line in f:
            yield [int(c) for c in line.strip()]

def get_counts(data, index):
    counts = Counter()
    for row in data:
        counts[row[index]] += 1

    return counts

def filter(data, bit_criteria):
    remaining = data
    for index in range(len(remaining[0])):
        counts = get_counts(remaining, index).most_common()
        if counts[0][1] == counts[1][1]:
            if bit_criteria == 0:
                target_value = 1
            else:
                target_value = 0
        else:
            target_value = counts[bit_criteria][0]

        remaining = [r for r in remaining if r[index] == target_value]
        if len(remaining) == 1:
            return remaining[0]

    raise ValueError()


def main(input_path):
    data = list(load_data(input_path))

    # msbs = []
    # lsbs = []

    # for index in range(len(data[0])):
    #     counts = get_counts(data, index).most_common()
    #     msbs.append(counts[0][0])
    #     lsbs.append(counts[1][0])

    # print(msbs)
    # print(lsbs)

    # gamma = int(''.join(str(c) for c in msbs), 2)
    # epsilon = int(''.join(str(c) for c in lsbs), 2)

    # answer = gamma * epsilon

    # print(f'g: {gamma}, e: {epsilon}, answer: {answer}')

    raw_oxy = ''.join(str(c) for c in filter(data, 0))
    oxy_gen = int(raw_oxy, 2)

    raw_co2 = ''.join(str(c) for c in filter(data, 1))
    co2_scrub = int(raw_co2, 2)

    answer = oxy_gen * co2_scrub

    print(f'o2: {oxy_gen}, co2: {co2_scrub}, answer: {answer}')

if __name__ == '__main__':
    main(sys.argv[1])