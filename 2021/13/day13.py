import sys
from typing import Tuple, Dict, List
from collections import defaultdict
from dataclasses import dataclass

@dataclass
class SparseGrid:
    grid: Dict[int, Dict[int, bool]]
    # max row & col values are inclusive
    max_row: int
    max_col: int

    def print(self):
        for row in range(self.max_row + 1):
            cells: List[str] = []
            for col in range(self.max_col + 1):
                if self.grid.get(row, {}).get(col):
                    cells.append('#')
                else:
                    cells.append('.')
            print(''.join(cells))

    def marks(self) -> int:
        total = 0
        for row in self.grid.values():
            total += sum(int(v) for v in row.values())

        return total

    def fold_up(self, row: int) -> 'SparseGrid':
        new_grid: Dict[int, Dict[int, bool]] = defaultdict(dict)
        new_max_rows = row - 1

        for grid_row in range(row):
            cols = self.grid.get(grid_row, {})
            fold_dist = row - grid_row

            # Find matching row below the fold
            below_fold = self.grid.get(row + fold_dist, {})

            # Merge the col dicts
            for col_index, val in cols.items():
                new_grid[grid_row][col_index] = val

            for col_index, val in below_fold.items():
                new_grid[grid_row][col_index] = val

        return SparseGrid(new_grid, new_max_rows, self.max_col)


    def fold_left(self, col: int) -> 'SparseGrid':
        new_grid: Dict[int, Dict[int, bool]] = defaultdict(dict)
        new_max_cols = col - 1

        rows = self.grid.keys()

        for grid_col in range(col):
            fold_dist = col - grid_col
            for row_index in rows:
                left_of_fold = self.grid[row_index].get(grid_col, False)
                right_of_fold = self.grid[row_index].get(col + fold_dist, False)

                if left_of_fold or right_of_fold:
                    new_grid[row_index][grid_col] = True

        return SparseGrid(new_grid, self.max_row, new_max_cols)


def load_data(input_path: str) -> Tuple[SparseGrid, List[Tuple[int, int]]]:
    max_row = 0
    max_col = 0
    grid: Dict[int, Dict[int, bool]] = defaultdict(dict)
    folds: List[Tuple[int, int]] = []
    with open(input_path, 'r') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                break

            x, y = (int(c) for c in stripped.split(','))
            if x > max_col:
                max_col = x
            if y > max_row:
                max_row = y
            grid[y][x] = True

        for line in f:
            tokens = line.strip().split(' ')
            if len(tokens) == 3:
                axis, val = tokens[2].split('=')
                if axis == 'x':
                    folds.append((0, int(val)))
                else:
                    folds.append((int(val), 0))

        return SparseGrid(grid, max_row, max_col), folds


def part1(input_path: str):
    grid, folds = load_data(input_path)
    grid.print()
    print(grid.marks())
    print(folds)

    for fold in folds:
        row, col = fold
        if row != 0:
            grid = grid.fold_up(row)
        else:
            grid = grid.fold_left(col)

    grid.print()




if __name__ == '__main__':
    part1(sys.argv[1])