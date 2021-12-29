import sys
from typing import List, Dict, Tuple
from itertools import groupby
from collections import defaultdict


def load_data(input_path: str) -> List[List[str]]:
    with open(input_path, 'r') as f:
        return [line.strip().split(' ') for line in f]


def is_valid(
    model_code: str,
    instructions: List[List[str]],
    target_z: int = 0
) -> bool:
    result = run([int(c) for c in model_code], instructions)
    return result['z'] == target_z


def run(
    input: List[int],
    instructions: List[List[str]],
    registers: Dict[str, int] = None
) -> Dict[str, int]:
    if registers:
        registers = dict(registers)
    else:
        registers = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

    def parse_val(arg: str) -> int:
        result = registers.get(arg)
        if result is None:
            return int(arg)
        else:
            return result

    input_iter = iter(input)

    for instruction in instructions:
        op = instruction[0]
        if op == 'inp':
            register = instruction[1]
            registers[register] = next(input_iter)
        elif op == 'add':
            arg1, arg2 = instruction[1:]
            new_val: int = registers[arg1] + parse_val(arg2)
            registers[arg1] = new_val
        elif op == 'mod':
            arg1, arg2 = instruction[1:]
            val1 = registers[arg1]
            val2 = parse_val(arg2)
            assert val1 >= 0
            assert val2 > 0
            new_val: int = val1 % val2
            registers[arg1] = new_val
        elif op == 'mul':
            arg1, arg2 = instruction[1:]
            new_val: int = registers[arg1] * parse_val(arg2)
            registers[arg1] = new_val
        elif op == 'div':
            arg1, arg2 = instruction[1:]
            val2 = parse_val(arg2)
            assert val2 != 0
            new_val: int = registers[arg1] // val2
            registers[arg1] = new_val
        elif op == 'eql':
            arg1, arg2 = instruction[1:]
            new_val = bool(registers[arg1] == parse_val(arg2))
            registers[arg1] = int(new_val)
        else:
            raise ValueError(f'Unexpected op: {op}')

    return registers


def search(
    reversed_input: List[Tuple[int, int]],
    states: List[Dict[int, Dict[int, int]]]
) -> List[str]:
    if not states:
        values = list(reversed([str(w) for z, w in reversed_input]))
        return [''.join(values)]

    result = []
    state = states[0]
    last_z_input, _ = reversed_input[-1]
    for prev_input in state[last_z_input].items():
        result.extend(search(reversed_input + [prev_input], states[1:]))

    return result


def build_lattice(
    instructions: List[List[str]]
) -> List[Dict[int, Dict[int, int]]]:
    # Split up instruction list into chunks starting with the inp w
    instruction_groups = []
    curr_group = []
    for inp_op, vals in groupby(instructions, key=lambda i: i[0] == 'inp'):
        if inp_op:
            if curr_group:
                instruction_groups.append(curr_group)
            curr_group = list(vals)
        else:
            curr_group.extend(vals)

    if curr_group:
        instruction_groups.append(curr_group)

    assert len(instruction_groups) == 14

    grouped_inst_count = sum(len(ig) for ig in instruction_groups)
    assert grouped_inst_count == len(instructions)

    # x and y register values going into the instruction group don't matter
    # because these get reset back to 0 before they are used

    # Maps between the z output value and the set of z, w input pairs that
    # create that output
    prev_z_states: Dict[int, Dict[int, int]] = {0: {}}
    all_states: List[Dict[int, Dict[int, int]]] = []
    ig_num = 1
    for ig in instruction_groups:
        print(f'Begin processing {ig_num}, states: {len(prev_z_states) * 10}')
        ig_num += 1
        states: Dict[int, Dict[int, int]] = defaultdict(dict)
        for z_val in prev_z_states:
            for w in range(1, 10):
                state = run([w], ig, {'w': 0, 'x': 0, 'y': 0, 'z': z_val})
                z_output = state['z']
                states[z_output][z_val] = w

        all_states.append(states)
        prev_z_states = states

    return all_states


def part2(input_path: str):
    instructions = load_data(input_path)
    all_states = build_lattice(instructions)
    reversed_states = list(reversed(all_states))

    last: Dict[int, Dict[int, int]] = reversed_states[0]
    target_z = 0

    min_value = '9' * len(reversed_states)
    input_states: Dict[int, int] = last[target_z]
    for input_state in input_states.items():
        best = min(search([input_state], reversed_states[1:]))
        if best < min_value:
            min_value = best

    checked = is_valid(min_value, instructions, target_z=target_z)
    print(f'Smallest value: {min_value}, is_valid: {checked}')


def part1(input_path: str):
    instructions = load_data(input_path)
    all_states = build_lattice(instructions)
    reversed_states = list(reversed(all_states))

    last: Dict[int, Dict[int, int]] = reversed_states[0]
    target_z = 0

    max_value = '0' * len(reversed_states)
    input_states: Dict[int, int] = last[target_z]
    for input_state in input_states.items():
        best = max(search([input_state], reversed_states[1:]))
        if best > max_value:
            max_value = best

    checked = is_valid(max_value, instructions, target_z=target_z)
    print(f'Biggest value: {max_value}, is_valid: {checked}')


if __name__ == '__main__':
    part2(sys.argv[1])