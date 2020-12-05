import sys
import re
from collections import Counter

FORMAT = re.compile(
    r'(?P<min>\d+)-(?P<max>\d+) (?P<char>\w): (?P<password>\w+)'
)

def load_data(input_path):
    with open(input_path, 'r') as f:
        for line in f:
            m = FORMAT.match(line).groupdict()
            yield int(m['min']), int(m['max']), m['char'], m['password'].strip()

def is_valid(min, max, c, pwd):
    occurrences = Counter(pwd)[c]
    return occurrences >= min and occurrences <= max

def is_valid2(min, max, c, pwd):
    print('****')
    print(f'{pwd[min-1]} == {c}')
    print(f'{pwd[max-1]} == {c}')
    return (pwd[min-1] == c) ^ (pwd[max-1] == c)

def main(input_path):
    matches = 0
    for min, max, c, pwd in load_data(input_path):
        if is_valid2(min, max, c, pwd):
            print(min, max, c, pwd)
            matches += 1

    print(matches)



if __name__ == '__main__':
    main(sys.argv[1])