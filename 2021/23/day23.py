import sys
import heapq
from collections import deque
from typing import Dict, List, Tuple, Set, ClassVar, Optional
from dataclasses import dataclass


@dataclass
class Burrow:
    ENERGY_COSTS: ClassVar[Dict[str, int]] = {
        'A': 1,
        'B': 10,
        'C': 100,
        'D': 1000
    }

    end_state: Dict[Tuple[int, int], str]
    positions: Dict[Tuple[int, int], str]
    energy: int

    def print(self):
        print('Current positions')
        self._print(self.positions)

        print('End state')
        self._print(self.end_state)

    def _print(self, points: Dict[Tuple[int, int], str]):
        max_rows = max(r for r, _ in points)
        max_cols = max(c for _, c in points)

        for r in range(max_rows + 1):
            row_vals = (
                points.get((r, c), ' ') for c in range(max_cols + 1)
            )
            print(''.join(row_vals))


    def is_winning_position(self) -> bool:
        return all(
            self.positions[pos] == amphipod
            for pos, amphipod in self.end_state.items()
        )

    def estimated_cost(self) -> int:
        min_possible_cost = 0
        for start_pos, amphipod in self.amphipod_positions():
            min_possible_cost += min(
                self._cost(amphipod, start_pos, end)
                for end in self.end_positions(amphipod)
            )

        return min_possible_cost


    def amphipod_positions(self):
        for s, a in self.positions.items():
            if a != '.':
                yield s, a

    def moves(self, min_costs) -> List['Burrow']:
        next_states = []

        for start, amphipod in self.amphipod_positions():
            for dest, dest_item in self.positions.items():
                move_cost = self._move_cost(amphipod, start, dest)
                if move_cost:
                    new_cost = self.energy + move_cost
                    new_positions = self.positions.copy()
                    new_positions[start] = '.'
                    new_positions[dest] = amphipod

                    canonical = tuple(sorted(new_positions.items()))
                    min_cost = min_costs.get(canonical)
                    if not min_cost or new_cost < min_cost:
                        min_costs[canonical] = new_cost
                        next_states.append(
                            Burrow(
                                end_state=self.end_state,
                                positions=new_positions,
                                energy=new_cost
                            )
                        )

        return next_states

    def end_positions(self, amphipod: str) -> Set[Tuple[int, int]]:
        return set(
            pos for pos, amp in self.end_state.items()
            if amp == amphipod
        )

    def _is_path_clear(self, start: Tuple[int, int], end: Tuple[int, int]):
        assert start[0] == end[0] or start[1] == end[1]

        row_diff = end[0] - start[0]
        if row_diff:
            row_incr = row_diff // abs(row_diff)
            pos = start
            while pos[0] != end[0]:
                pos = (pos[0] + row_incr, pos[1])
                if self.positions[pos] != '.':
                    return False

        col_diff = end[1] - start[1]
        if col_diff:
            col_incr = col_diff // abs(col_diff)
            pos = start
            while pos[1] != end[1]:
                pos = (pos[0], pos[1] + col_incr)
                if self.positions[pos] != '.':
                    return False

        return True

    def _move_cost(
        self,
        amphipod: str,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> Optional[int]:
        # Destination cannot be occupied
        if self.positions[end] != '.':
            return None

        start_in_room = start in self.end_state
        if start_in_room and end[1] == start[1]:
            # Cannot stop directly outside room
            return None

        if start_in_room and end in self.end_state:
            # For now, do not allow starting and ending in a room on the same
            # move.
            return None

        if not start_in_room:
            end_positions = self.end_positions(amphipod)
            if end not in end_positions:
                # Once in the hallway, next move must be back to target side room
                return None

            # Must move as deep into the room as possible
            next = (end[0] + 1, end[1])
            if self.end_state.get(next) == '.':
                print(f'Could have moved deeper into room. Skipping {end}')
                return None

            # Cannot move back into the target side room unless empty or only
            # contains appropriate type of amphipods
            for side_room_pos in end_positions:
                end_cell = self.positions[side_room_pos]
                if end_cell != amphipod and end_cell != '.':
                    return None


        if start_in_room:
            # Align on row first, then align on col
            intermediate_pos = (end[0], start[1])
            if not self._is_path_clear(start, intermediate_pos):
                return None

            if not self._is_path_clear(intermediate_pos, end):
                return None
        else:
            # Align on col first, then move down
            intermediate_pos = (start[0], end[1])
            if not self._is_path_clear(start, intermediate_pos):
                return None

            if not self._is_path_clear(intermediate_pos, end):
                return None

        # Path is valid, count up the steps
        return self._cost(amphipod, start, end)

    def _cost(
        self,
        amphipod: str,
        start: Tuple[int, int],
        end: Tuple[int, int]
    ) -> int:
        steps = abs(end[0] - start[0]) + abs(end[1] - start[1])
        return steps * self.ENERGY_COSTS[amphipod]

def extract_positions(world: List[str]) -> Burrow:
    amphipod_types = ['A', 'B', 'C', 'D']
    amphipod_iter = iter(amphipod_types)
    side_rooms = {}
    end_state = {}
    positions = {}
    for r in range(len(world)):
        for c in range(len(world[r])):
            cell = world[r][c]
            if cell in amphipod_types:
                side_room = side_rooms.get(c)
                if not side_room:
                    side_room = next(amphipod_iter)
                    side_rooms[c] = side_room
                end_state[(r, c)] = side_room
                positions[(r, c)] = cell
            elif cell == '.':
                positions[(r, c)] = cell

    return Burrow(
        end_state=end_state,
        positions=positions,
        energy=0
    )


def load_data(input_path: str) -> Burrow:
    with open(input_path, 'r') as f:
        return [line.rstrip('\n') for line in f]



def part1(input_path: str):
    world = load_data(input_path)
    burrow = extract_positions(world)

    entry = 0
    frontier = []
    heapq.heappush(frontier, (burrow.estimated_cost(), entry, burrow))
    entry += 1

    winning_state = None
    min_cost_cache = {}
    while frontier:
        estimate, _, state = heapq.heappop(frontier)
        print(f'Evaluating state with estimate: {estimate}')
        if state.is_winning_position():
            print(f'Found winning position: {state}')
            winning_state = state
            break

        for next_state in state.moves(min_cost_cache):
            cost = next_state.energy + next_state.estimated_cost()
            heapq.heappush(frontier, (cost, entry, next_state))
            entry += 1

    print(f'Min energy: {winning_state.energy}')


def part2(input_path: str):
    world = load_data(input_path)
    world = (
        world[:3] +
        [
            "  #D#C#B#A#",
            "  #D#B#A#C#"
        ] +
        world[3:]
    )
    burrow = extract_positions(world)
    burrow.print()

    entry = 0
    frontier = []
    heapq.heappush(frontier, (burrow.estimated_cost(), entry, burrow))
    entry += 1

    winning_state = None
    min_cost_cache = {}
    while frontier:
        estimate, _, state = heapq.heappop(frontier)
        print(f'Evaluating state with estimate: {estimate}')
        if state.is_winning_position():
            print(f'Found winning position: {state}')
            winning_state = state
            break

        for next_state in state.moves(min_cost_cache):
            cost = next_state.energy + next_state.estimated_cost()
            heapq.heappush(frontier, (cost, entry, next_state))
            entry += 1

    print(f'Min energy: {winning_state.energy}')
    winning_state.print()

if __name__ == '__main__':
    part1(sys.argv[1])