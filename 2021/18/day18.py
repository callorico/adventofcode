import sys
from typing import Union, Tuple, List, Optional
from dataclasses import dataclass
from itertools import permutations
from copy import deepcopy


@dataclass
class SnailNumber:
    _left: Union[int, 'SnailNumber']
    _right: Union[int, 'SnailNumber']
    _parent: Optional['SnailNumber']

    def __init__(self, left: 'SnailNumber', right: 'SnailNumber'):
        self.left = left
        self.right = right

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, val: Union[int, 'SnailNumber']):
        self._left = val
        if not isinstance(val, int):
            val._parent = self

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, val: Union[int, 'SnailNumber']):
        self._right = val
        if not isinstance(val, int):
            val._parent = self

    @property
    def parent(self):
        return self._parent

    def add(self, n: 'SnailNumber') -> 'SnailNumber':
        return SnailNumber(left=self, right=n)

    def magnitude(self) -> int:
        left = self.left
        right = self.right

        if not isinstance(left, int):
            left = left.magnitude()

        if not isinstance(right, int):
            right = right.magnitude()

        return (3 * left) + (2 * right)

    def reduce(self):
        while True:
            exploded = self._explode()
            split = False
            if not exploded:
                split = self._split()

            if not exploded and not split:
                return

    def _explode(self) -> bool:
        ordering = self._traversal(0)

        for i in range(len(ordering)):
            depth, values, number = ordering[i]
            if depth == 4:
                prev = None
                if i > 0:
                    _, prev_values, prev = ordering[i - 1]

                next = None
                if i < len(ordering) - 1:
                    _, next_values, next = ordering[i + 1]

                if prev:
                    if isinstance(prev.right, int):
                        prev.right += values[0]
                    else:
                        prev.left += values[0]

                if next:
                    if isinstance(next.left, int):
                        next.left += values[1]
                    else:
                        next.right += values[1]

                if number.parent:
                    if number.parent.left is number:
                        number.parent.left = 0
                    elif number.parent.right is number:
                        number.parent.right = 0

                return True

        return False

    def _split(self) -> bool:
        def divide(val) -> 'SnailNumber':
            round_down = val // 2
            return SnailNumber(left=round_down, right=val - round_down)

        ordering = self._traversal(0)
        for _, _, number in ordering:
            if isinstance(number.left, int) and number.left >= 10:
                number.left = divide(number.left)
                return True

            if isinstance(number.right, int) and number.right >= 10:
                number.right = divide(number.right)
                return True

        return False

    def _traversal(self, depth: int):
        if isinstance(self.left, int):
            left_val = self.left
        else:
            left_val = None

        if isinstance(self.right, int):
            right_val = self.right
        else:
            right_val = None

        ordering = []
        if left_val is None:
            ordering.extend(self.left._traversal(depth + 1))

        if left_val is not None or right_val is not None:
            ordering.append((depth, (left_val, right_val), self))

        if right_val is None:
            ordering.extend(self.right._traversal(depth + 1))

        return ordering

    def __repr__(self):
        contents = '['
        if isinstance(self.left, int):
            contents += str(self.left)
        else:
            contents += repr(self.left)

        contents += ','

        if isinstance(self.right, int):
            contents += str(self.right)
        else:
            contents += repr(self.right)

        contents += ']'

        return contents


def load_data(input_path: str) -> List[SnailNumber]:
    def parse(raw: str, index: int) -> Tuple[SnailNumber, int]:
        assert raw[index] == '['
        curr = index + 1
        elements = []
        while raw[curr] != ']':
            if raw[curr] == '[':
                element, new_index = parse(raw, curr)
                elements.append(element)
                curr = new_index
            elif raw[curr] == ',':
                curr += 1
            else:
                elements.append(int(raw[curr]))
                curr += 1

        assert len(elements) == 2
        return SnailNumber(left=elements[0], right=elements[1]), curr + 1

    with open(input_path, 'r') as f:
        return [parse(line, 0)[0] for line in f]


def part1(input_path: str):
    numbers = load_data(input_path)

    sum: SnailNumber = numbers[0]
    for n in numbers[1:]:
        sum = sum.add(n)
        sum.reduce()

    print(f'sum: {sum}')
    print(sum.magnitude())

def part2(input_path: str):
    numbers = load_data(input_path)

    max = 0

    for a, b in permutations(numbers, 2):
        a2 = deepcopy(a)
        b2 = deepcopy(b)
        print(f'a: {a2}, b: {b2}')
        a2 = a2.add(b2)
        a2.reduce()
        magnitude = a2.magnitude()
        if magnitude > max:
            print(f'new max {magnitude}')
            max = magnitude

    print(max)





if __name__ == '__main__':
    #part1(sys.argv[1])
    part2(sys.argv[1])