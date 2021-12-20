from dataclasses import dataclass
import sys
import re
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass
from itertools import product

SCANNER_RE = re.compile(r'scanner (?P<scanner>\d+)')

@dataclass
class Matrix:
    contents: Tuple[Tuple[int, ...], ...]

    def multiply(self, b: 'Matrix') -> 'Matrix':
        rows = len(self.contents)
        cols = len(b.contents[0])

        product_rows = []
        for r in range(rows):
            product_row = []
            for c in range(cols):
                col_vec = (b.contents[br][c] for br in range(rows))
                product_row.append(
                    sum(a * b for a, b in zip(self.contents[r], col_vec))
                )

            product_rows.append(tuple(product_row))

        return Matrix(tuple(product_rows))

    def difference(self, b: 'Matrix') -> 'Matrix':
        result = []
        for r1, r2 in zip(self.contents, b.contents):
            row = tuple(v1 - v2 for v1, v2 in zip(r1, r2))
            result.append(row)

        return Matrix(tuple(result))

    def __getitem__(self, key) -> Tuple[int, ...]:
        return self.contents[key]

    def __hash__(self) -> int:
        return hash(self.contents)

    def __eq__(self, other: 'Matrix') -> bool:
        return self.contents == getattr(other, 'contents', None)


def load_data(input_path: str) -> List[List[Matrix]]:
    scanners = []
    with open(input_path, 'r') as f:
        while line := f.readline():
            m = SCANNER_RE.search(line)
            scanner = int(m.group('scanner'))
            assert scanner == len(scanners)
            coordinates = []
            while (line := f.readline().strip()) != '':
                v = Matrix(tuple(
                    (int(c),) for c in line.split(',')
                ))
                coordinates.append(v)

            scanners.append(coordinates)

    return scanners

def update_beacons(
    rotations: List[Matrix],
    rotation_cache: Dict[int, List[Matrix]],
    canonical_beacons: Set[Matrix],
    sensor_id: int,
    new_sensor: List[Matrix]
):
    for rotation in rotations:
        rotated_points = rotation_cache.get((sensor_id, rotation))
        if not rotated_points:
            rotated_points = [rotation.multiply(p) for p in new_sensor]
            rotation_cache[(sensor_id, rotation)] = rotated_points

        # Figure out if we have sufficient beacon overlap to call this a match
        for p1 in rotated_points:
            for p2 in canonical_beacons:
                offset = p1.difference(p2)
                offset_points = set(p.difference(offset) for p in rotated_points)
                if len(offset_points.intersection(canonical_beacons)) >= 12:
                    # Found a matching orientation!
                    # Insert all of the rotated and offset points into the
                    # canonical set
                    canonical_beacons.update(offset_points)
                    return offset

    return None


def part2(input_path: str):
    x_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, 0, -1),
                (0, 1, 0)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, -1, 0),
                (0, 0, -1)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, 0, 1),
                (0, -1, 0)
            )
        ),
    ]
    y_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, 0, 1),
                (0, 1, 0),
                (-1, 0, 0)
            )
        ),
        Matrix(
            (
                (-1, 0, 0),
                (0, 1, 0),
                (0, 0, -1)
            )
        ),
        Matrix(
            (
                (0, 0, -1),
                (0, 1, 0),
                (1, 0, 0)
            )
        ),
    ]
    z_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, -1, 0),
                (1, 0, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (-1, 0, 0),
                (0, -1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, 1, 0),
                (-1, 0, 0),
                (0, 0, 1)
            )
        ),
    ]

    rotations = set()
    for x, y, z in product(x_rotations, y_rotations, z_rotations):
        rotations.add(x.multiply(y).multiply(z))

    assert len(rotations) == 24
    scanners = load_data(input_path)

    beacons = set(scanners[0])

    canonical_scanners = [Matrix(((0,),(0,),(0,)))]
    cache = {}
    remaining = [(i + 1, points) for i, points in enumerate(scanners[1:])]
    while remaining:
        for scanner in remaining:
            scanner_index, scanner_points = scanner
            print(f'Checking scanner {scanner_index} for overlaps')
            canonical_scanner = update_beacons(
                rotations,
                cache,
                beacons,
                scanner_index,
                scanner_points,
            )
            if canonical_scanner:
                print(f'matched! {canonical_scanner}')
                canonical_scanners.append(canonical_scanner)
                break

        remaining.remove(scanner)


    max_distance = 0
    for i in range(len(canonical_scanners)):
        for j in range(i, len(canonical_scanners)):
            diff = canonical_scanners[i].difference(canonical_scanners[j])
            manhattan = abs(diff[0][0]) + abs(diff[1][0]) + abs(diff[2][0])
            if manhattan > max_distance:
                max_distance = manhattan
                print(f'max: {max_distance}')

    print(f'Distance: {max_distance}')


def part1(input_path: str):
    x_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, 0, -1),
                (0, 1, 0)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, -1, 0),
                (0, 0, -1)
            )
        ),
        Matrix(
            (
                (1, 0, 0),
                (0, 0, 1),
                (0, -1, 0)
            )
        ),
    ]
    y_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, 0, 1),
                (0, 1, 0),
                (-1, 0, 0)
            )
        ),
        Matrix(
            (
                (-1, 0, 0),
                (0, 1, 0),
                (0, 0, -1)
            )
        ),
        Matrix(
            (
                (0, 0, -1),
                (0, 1, 0),
                (1, 0, 0)
            )
        ),
    ]
    z_rotations = [
        Matrix(
            (
                (1, 0, 0),
                (0, 1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, -1, 0),
                (1, 0, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (-1, 0, 0),
                (0, -1, 0),
                (0, 0, 1)
            )
        ),
        Matrix(
            (
                (0, 1, 0),
                (-1, 0, 0),
                (0, 0, 1)
            )
        ),
    ]

    rotations = set()
    for x, y, z in product(x_rotations, y_rotations, z_rotations):
        rotations.add(x.multiply(y).multiply(z))

    assert len(rotations) == 24
    scanners = load_data(input_path)

    beacons = set(scanners[0])

    cache = {}
    remaining = [(i + 1, points) for i, points in enumerate(scanners[1:])]
    while remaining:
        for scanner in remaining:
            scanner_index, scanner_points = scanner
            print(f'Checking scanner {scanner_index} for overlaps')
            if update_beacons(
                rotations,
                cache,
                beacons,
                scanner_index,
                scanner_points):
                print(f'matched!')
                break

        remaining.remove(scanner)

    print(beacons)
    print(len(beacons))


if __name__ == '__main__':
    part2(sys.argv[1])