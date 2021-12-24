import sys
from typing import Tuple, List, Optional
from dataclasses import dataclass

@dataclass
class Cuboid:
    x_range: Tuple[int, int]
    y_range: Tuple[int, int]
    z_range: Tuple[int, int]
    on: bool

    def inside(self, x: int, y: int, z: int) -> bool:
        return (
            x >= self.x_range[0] and x <= self.x_range[1]
            and y >= self.y_range[0] and y <= self.y_range[1]
            and z >= self.z_range[0] and z <= self.z_range[1]
        )

    @property
    def volume(self) -> int:
        return (
            (self.x_range[1] - self.x_range[0] + 1) *
            (self.y_range[1] - self.y_range[0] + 1) *
            (self.z_range[1] - self.z_range[0] + 1)
        )

    def overlay(self, other: 'Cuboid') -> List['Cuboid']:
        """Overlays the specified cuboid on top of this one and splits this
        one into a set of cuboids that do not overlap with the specified
        one."""
        overlap_x = self._overlap(self.x_range, other.x_range)
        if not overlap_x:
            return [self]

        overlap_y = self._overlap(self.y_range, other.y_range)
        if not overlap_y:
            return [self]

        overlap_z = self._overlap(self.z_range, other.z_range)
        if not overlap_z:
            return [self]

        splits = []
        if overlap_z[1] + 1 <= self.z_range[1]:
            splits.append(
                Cuboid(
                    x_range=self.x_range,
                    y_range=self.y_range,
                    z_range=(overlap_z[1] + 1, self.z_range[1]),
                    on=self.on
                )
            )

        if overlap_z[0] - 1 >= self.z_range[0]:
            splits.append(
                Cuboid(
                    x_range=self.x_range,
                    y_range=self.y_range,
                    z_range=(self.z_range[0], overlap_z[0] - 1),
                    on=self.on
                )
            )

        if overlap_y[1] + 1 <= self.y_range[1]:
            splits.append(
                Cuboid(
                    x_range=self.x_range,
                    y_range=(overlap_y[1] + 1, self.y_range[1]),
                    z_range=overlap_z,
                    on=self.on
                )
            )

        if overlap_y[0] - 1 >= self.y_range[0]:
            splits.append(
                Cuboid(
                    x_range=self.x_range,
                    y_range=(self.y_range[0], overlap_y[0] - 1),
                    z_range=overlap_z,
                    on=self.on
                )
            )

        if overlap_x[1] + 1 <= self.x_range[1]:
            splits.append(
                Cuboid(
                    x_range=(overlap_x[1] + 1, self.x_range[1]),
                    y_range=overlap_y,
                    z_range=overlap_z,
                    on=self.on
                )
            )

        if overlap_x[0] - 1 >= self.x_range[0]:
            splits.append(
                Cuboid(
                    x_range=(self.x_range[0], overlap_x[0] - 1),
                    y_range=overlap_y,
                    z_range=overlap_z,
                    on=self.on
                )
            )

        # As a sanity check, the sum of the split cuboids plus the overlap
        # cuboid's volume should equal self.volume
        intersect = Cuboid(overlap_x, overlap_y, overlap_z, self.on)
        disjoint_vol = sum(s.volume for s in splits) + intersect.volume
        assert disjoint_vol == self.volume

        return splits


    def _overlap(
        self,
        a: Tuple[int, int],
        b: Tuple[int, int]
    ) -> Optional[Tuple[int, int]]:
        a_min, a_max = a
        b_min, b_max = b

        if a_max < b_min:
            return None

        if a_min > b_max:
            return None

        return (max(a_min, b_min), min(a_max, b_max))

    def __hash__(self):
        return hash((self.x_range, self.y_range, self.z_range))

    def __eq__(self, other: 'Cuboid'):
        return (
            self.x_range == other.x_range and
            self.y_range == other.y_range and
            self.z_range == other.z_range
        )

def load_data(input_path: str) -> List[Cuboid]:
    with open(input_path, 'r') as f:
        results = []
        for line in f:
            state, coords = line.strip().split(' ')
            xrange, yrange, zrange = coords.split(',')
            xmin, xmax = (int(v) for v in xrange.split('=')[1].split('..'))
            ymin, ymax = (int(v) for v in yrange.split('=')[1].split('..'))
            zmin, zmax = (int(v) for v in zrange.split('=')[1].split('..'))

            results.append(
                (
                    Cuboid(
                        x_range=(xmin, xmax),
                        y_range=(ymin, ymax),
                        z_range=(zmin, zmax),
                        on=(state == 'on')
                    )
                )
            )

        return results


def part2(input_path: str):
    data = load_data(input_path)

    disjoint_cuboids = [data[0]]
    for cuboid in data[1:]:
        new_disjoint_cuboids = []
        for existing in disjoint_cuboids:
            new_disjoint_cuboids.extend(existing.overlay(cuboid))
        new_disjoint_cuboids.append(cuboid)
        disjoint_cuboids = new_disjoint_cuboids

    total_volume = sum(c.volume for c in disjoint_cuboids if c.on)
    print(f'total volume: {total_volume}')


def part1(input_path: str):
    data = load_data(input_path)

    cubes_on = set()
    for x in range(-50, 50 + 1):
        for y in range(-50, 50 + 1):
            for z in range(-50, 50 + 1):
                for cuboid in data:
                    if cuboid.inside(x, y, z):
                        if cuboid.on:
                            cubes_on.add((x, y, z))
                        else:
                            cubes_on.discard((x, y, z))
    print(f'Cubes on: {len(cubes_on)}')

if __name__ == '__main__':
    part2(sys.argv[1])