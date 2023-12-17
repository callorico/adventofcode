from __future__ import annotations
import sys
import bisect
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class Range:
    start: int
    length: int

    @property
    def end(self):
        """The endpoint of the range, inclusive"""
        return self.start + self.length
    
    def intersect(self, other: Range) -> Optional[Range]:
        if other.start > self.end or other.end < self.start:
            return None

        start = max(self.start, other.start) 
        end = min(self.end, other.end)
        return Range(start=start, length=end - start)


class SparseMap:
    def __init__(self, ranges: list[list[int]], label: str):
        self.label: str = label.strip()
        self.ranges: list[Tuple[Range, int]] = [(Range(start=r[1], length=r[2]), r[1] - r[0]) for r in ranges]

    def __repr__(self):
        return f"{self.label} -> {self.ranges}"
    
    def convert(self, source: list[Range]) -> list[Range]:
        converted: list[Range] = []

        original_length = sum(r.length for r in source)

        for mapped_range, offset in self.ranges:
            remaining_unmapped_ranges = []
            for range in source:
                intersect = range.intersect(mapped_range)
                if intersect:
                    converted.append(Range(intersect.start - offset, intersect.length))
                    if intersect.start > range.start:
                        remaining_unmapped_ranges.append(Range(start=range.start, length=intersect.start - range.start))
                    if intersect.end < range.end:
                        remaining_unmapped_ranges.append(Range(start=intersect.end, length=range.end- intersect.end))
                else:
                    remaining_unmapped_ranges.append(range)

            source = remaining_unmapped_ranges

        # Tack on any remaining unconverted ranges
        converted.extend(source)

        # Sanity check. Total lengths should remain unchanged
        converted_length = sum(r.length for r in converted)
        assert original_length == converted_length, "Total length of input ranges should remain unchanged after conversion"

        return converted 


def parse_numbers(number_text: str) -> list[int]:
    return [int(n) for n in number_text.split(" ") if n]


def parse_map(f, label: str) -> SparseMap:
    ranges: list[list[int]] = []
    while True:
        line = f.readline().strip()
        if not line:
            return SparseMap(ranges, label)

        ranges.append(parse_numbers(line))


def load_data(input_path) -> Tuple[list[Range], list[SparseMap]]:
    with open(input_path, "r") as f:
        seeds_text = f.readline()
        seeds: list[int] = parse_numbers(seeds_text.split(": ", 1)[1])

        f.readline()
        mappings = []
        while True:
            label = f.readline()
            if not label:
                break
            mappings.append(parse_map(f, label))

        parsed_seeds = [Range(start=seeds[i], length=seeds[i+1]) for i in range(0, len(seeds), 2)]

        return parsed_seeds, mappings


def main(input_path):
    seeds, mappings = load_data(input_path)

    total_seeds = sum(s.length for s in seeds)

    curr_min: Optional[int] = None
    mapped: list[Range] = seeds

    # Apply mappings between elements until we get to location
    for mapping in mappings:
        mapped = mapping.convert(mapped)

    # Sanity check to make sure we haven't dropped any seeds
    total_mapped_locations = sum(m.length for m in mapped)
    assert total_seeds == total_mapped_locations

    # Find min of all converted ranges
    min_location = min(mapped, key=lambda r: r.start)
    if curr_min is None or min_location.start < curr_min:
        curr_min = min_location.start

    print(f"Min location value is: {curr_min}")


if __name__ == "__main__":
    main(sys.argv[1])