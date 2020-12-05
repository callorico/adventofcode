import sys
import re
from collections import Counter


    # byr (Birth Year) - four digits; at least 1920 and at most 2002.
    # iyr (Issue Year) - four digits; at least 2010 and at most 2020.
    # eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
    # hgt (Height) - a number followed by either cm or in:
    #     If cm, the number must be at least 150 and at most 193.
    #     If in, the number must be at least 59 and at most 76.
    # hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
    # ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
    # pid (Passport ID) - a nine-digit number, including leading zeroes.
    # cid (Country ID) - ignored, missing or not.

ECL_SET = set([
    'amb',
    'blu',
    'brn',
    'gry',
    'grn',
    'hzl',
    'oth'
])

def byr(val):
    try:
        year = int(val)
    except ValueError:
        return False
    else:
        return year >= 1920 and year <= 2002

def iyr(val):
    try:
        year = int(val)
    except ValueError:
        return False
    else:
        return year >= 2010 and year <= 2020

def eyr(val):
    try:
        year = int(val)
    except ValueError:
        return False
    else:
        return year >= 2020 and year <= 2030

def hgt(val):
    number = val[0:-2]
    unit = val[-2:]

    try:
        height = int(number)
    except ValueError:
        return False
    else:
        if unit == 'cm':
            return height >= 150 and height <= 193
        elif unit == 'in':
            return height >= 59 and height <= 76
        else:
            return False

def hcl(val):
    m = re.match(r'#[0-9a-f]{6}$', val)
    return m is not None


def ecl(val):
    return val in ECL_SET


def pid(val):
    m = re.match(r'\d{9}$', val)
    return m is not None


def cid(val):
    return True


def load_data(input_path):
    with open(input_path, 'r') as f:
        passport = {}
        for line in f:
            if not line.strip():
                yield passport
                passport = {}
            pairs = line.split()
            for pair in pairs:
                key, value = pair.split(':')
                passport[key] = value

        yield passport


def is_valid(passport):
    if (len(passport) == 8 or
            len(passport) == 7 and 'cid' not in passport):
        for key, value in passport.items():
            validator = globals().get(key, lambda v: False)
            result = validator(value)
            if not result:
                print(f'Failed validator {key}')
                return False

        return True
    else:
        return False

    # if len(passport) > 8:
    #     # print('Too many keys')
    #     return False

    # if len(passport) == 7 and 'cid' not in passport:
    #     # print('missing keys')
    #     return False

    # if len(passport) < 7:
    #     # print('Too few keys')
    #     return False

    # for key, value in passport.items():
    #     validator = globals().get(key, lambda v: False)
    #     result = validator(value)
    #     if not result:
    #         print(f'Failed validator {key}')
    #         return False

    return True


def main(input_path):
    count = 0
    for passport in load_data(input_path):
        result = is_valid(passport)
        print(f'{passport}: {result}')
        if result:
            count += 1

    print(count)


if __name__ == '__main__':
    main(sys.argv[1])