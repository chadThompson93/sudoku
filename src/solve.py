"""
Util functions to solve a Sudoku grid using the backtracking algorithm
Functions used in board.py
"""


def print_board(board):
    """
    :param board: 2D array representing Sudoku board

    Prints board
    """
    for row in range(9):
        r = ""
        for col in range(9):
            r += str(board[row][col]) + " "
        print(r)


def find_vacant_cell(board):
    """
    :param board: 2D array representing Sudoku board
    :return: returns cordinates of the first vacant position

    Searches board for a 0/vacant position.
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                vacant_position = [row, col]
                return vacant_position
    return [-1, -1]


"checks if the number exists in the row, the column, and the sub 3x3 matrix"


def check_position(number, row, col, board):
    """
    :param number: number to be entered into the board
    :param row: number row position
    :param col: number col position
    :param board: 2D array representing Sudoku board
    :return: True if it number follows rule of sudoku and False if not

    Checks if entering the number at the row, col position into the board follows the rules of Sudoku
    """
    for c in range(9):
        if board[row][c] == number:
            return False

    for r in range(9):
        if board[r][col] == number:
            return False

    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if board[r][c] == number:
                return False

    return True


def check_board(board):
    """
    :param board: 2D array representing Sudoku board
    :return: True if board is filled False if not

    checks if the board is completely filled(no 0s)
    """
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False

    return True


def find_number(board, num):
    """
    :param board: 2D array representing Sudoku board
    :param num: number to be found
    :return: positions of all cells that have the num in it

    Used to find the position of all cells with the num in it
    """
    positions = []
    for row in range(9):
        for col in range(9):
            if board[row][col] == num:
                positions.append((col, row))
    return positions


def solve(board):
    """
    :param board: 2D array representing Sudoku board
    :return: True if solved, False if the board is not solvable

    Solves the Sudoku board using recursion and backtracking

    Backtracking description:
        Finds first vacant cells using find_vacant_cell into vacant_position
        then on that current cell for each number 1-9 check if it satisfies the rules of sudoku using
        check_position() if the rules are satisfied insert it into the board then call solve using the updated board
        and proceed. If number does not satisfy the rules of Sudoku reset value back to 0.
    """
    vacant_position = find_vacant_cell(board)
    if vacant_position[0] == -1:
        return True
    row = vacant_position[0]
    col = vacant_position[1]
    for i in range(1, 10):
        if check_position(i, row, col, board):
            board[row][col] = i

            if solve(board):
                return True

            board[row][col] = 0
    return False
