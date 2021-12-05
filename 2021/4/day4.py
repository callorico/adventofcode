import sys
from typing import Dict, Tuple, List, Optional

Board = List[List[Tuple[int, bool]]]

def load_data(input_path):
    with open(input_path, 'r') as f:
        drawn_numbers = [int(c) for c in f.readline().split(',')]
        print(drawn_numbers)

        boards = []
        # lookup: Dict[int, List[Tuple[int, int, int]]] = {}

        while f.readline() != '':
            board = []
            for _ in range(5):
                row = [(int(c), False) for c in f.readline().split()]
                board.append(row)
            boards.append(board)

    return drawn_numbers, boards

def is_winner(board: Board) -> bool:
    for i in range(len(board)):
        # Check rows with index i
        if all(mark for _, mark in board[i]):
            return True

        # Check column with index i
        col = [r[i][1] for r in board]
        if all(col):
            return True

    return False


def find_winners(boards: List[Board]) -> List[Board]:
    matches = []
    for board in boards:
        if is_winner(board):
            matches.append(board)

    return matches

#     return None
# def find_winner(boards: List[Board]) -> Optional[Board]:
#     for board in boards:
#         if is_winner(board):
#             return board

#     return None

def score(board: Board) -> int:
    total = 0
    for row in range(len(board)):
        for col in range(len(board)):
            if not board[row][col][1]:
                total += board[row][col][0]

    return total


def mark_boards(ball: int, boards: List[Board]):
    for board in boards:
        for row in range(len(board)):
            for col in range(len(board)):
                if board[row][col][0] == ball:
                    board[row][col] = (ball, True)

def main(input_path):
    drawn_numbers, boards = load_data(input_path)

    for ball in drawn_numbers:
        print(f'Drawn: {ball}')
        mark_boards(ball, boards)
        # winner = find_winner(boards)
        # if winner:
        #     print(winner)
        #     print(score(winner) * ball)
        #     break
        for winner in find_winners(boards):
            if len(boards) == 1:
                print(boards[0])
                print(score(boards[0]) * ball)
                return
            boards.remove(winner)


if __name__ == '__main__':
    main(sys.argv[1])