from src import solve
import pygame
from src.solve import *


class Board:
    """
    Sudoku board class allows for inserting numbers into board, delete, check correctness of board state, and find all
    numbers similar to the one selected
    """
    # colors used in Sudoku board
    BLACK = (50, 50, 50)
    WHITE = (255, 255, 255)
    LIGHTGRAY = (100, 100, 100)

    def __init__(self, width, height, square_si, cell_si, win, grid):
        """
        :param width: width of entire board
        :param height: height of entire board
        :param square_si: dimensions of 3x3 squares on sudoku board
        :param cell_si: dimensions of individual cells
        :param win: game Window reference
        :param grid: sudoku numbers given in form in 2d array 0s represent empty spaces

        Initializes dimensions of the board
        initialize location of original numbers of the board: original_numbers
        Initialize solved board: solved_board
        Initialize current clicked square: selected
        Initialize list used to find similar numbers to selected: selected_num_pos
        """
        self.board_width = width
        self.board_height = height
        self.square_size = square_si
        self.cell_size = cell_si
        self.window = win
        self.board = grid[:]
        self.selected = (-1, -1)
        self.original_numbers = []
        self.selected_num_pos = []
        self.temp = None
        for i in range(9):
            temp = []
            for j in range(9):
                if self.board[i][j] != 0:
                    temp.append(1)
                else:
                    temp.append(0)
            self.original_numbers.append(temp)
        self.solved_board = []
        for i in range(9):
            temp = []
            for j in range(9):
                temp.append(self.board[i][j])
            self.solved_board.append(temp)
        solve(self.solved_board)

    def draw_grid(self):
        """
        Draws the entire board using pygame library draw.line function
        Draws red squares around selected cells using pygame library
        """
        fnt = pygame.font.SysFont("comicsans", 40)

        # draw the lines of the sudoku board WHITE lines are the boarder and LIGHTGRAY lines are the inner lines
        for x in range(0, self.board_width, self.cell_size):
            pygame.draw.line(self.window, self.LIGHTGRAY, (x, 0), (x, self.board_height))
        for y in range(0, self.board_height, self.cell_size):
            pygame.draw.line(self.window, self.LIGHTGRAY, (0, y), (self.board_width, y))

        for x in range(0, self.board_width, self.square_size):
            pygame.draw.line(self.window, self.WHITE, (x, 0), (x, self.board_height))
        for y in range(0, self.board_height, self.square_size):
            pygame.draw.line(self.window, self.WHITE, (0, y), (self.board_width, y))
        pygame.draw.line(self.window, self.WHITE, (0, self.board_height), (self.board_width, self.board_height))

        # draws the numbers in each individual cell
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    text = fnt.render(str(self.board[row][col]), 1, self.WHITE)
                    self.window.blit(text, (col * self.cell_size + (self.cell_size // 2 - text.get_width() / 2),
                                            row * self.cell_size + (self.cell_size // 2 - text.get_height() / 2)))

        # if there are more than one instance of the selected number on the board highlight them for user by drawing
        # red rectangle around them
        # if there is a temp value then draw that into the selected cell
        if self.selected_num_pos:
            for col, row in self.selected_num_pos:
                pygame.draw.rect(self.window, (255, 0, 0),
                                 (col * self.cell_size, row * self.cell_size, self.cell_size,
                                  self.cell_size), 3)
            if self.temp is not None:
                text = fnt.render(str(self.temp), 1, self.LIGHTGRAY)
                self.window.blit(text, (self.selected[0] * self.cell_size + 5, self.selected[1] * self.cell_size + 5))

        # if there is only one instance of the selected number draw red rectangle around it
        # if there is a temp value then draw that into the selected cell
        if self.selected[0] != -1 and not self.selected_num_pos:
            pygame.draw.rect(self.window, (255, 0, 0),
                             (self.selected[0] * self.cell_size, self.selected[1] * self.cell_size, self.cell_size,
                              self.cell_size), 3)
            if self.temp is not None:
                text = fnt.render(str(self.temp), 1, self.LIGHTGRAY)
                self.window.blit(text, (self.selected[0] * self.cell_size + 5, self.selected[1] * self.cell_size + 5))

    def click(self, pos):
        """
        :param pos: x, y cordinates of the click

        Determines if the click is within the boarders of the board grabs position. If the position on the board is not
        empty, call find_number() to find the position of all positions on the board that have the same number of the
        original position cited in pos

        """
        self.temp = None
        if pos[0] < self.board_width and pos[1] < self.board_height:
            x = pos[0] // self.cell_size
            y = pos[1] // self.cell_size
            self.selected = (x, y)
            if self.board[y][x] != 0:
                self.selected_num_pos = find_number(self.board, self.board[y][x])
            else:
                self.selected_num_pos = []
        else:
            self.selected = (-1, -1)
            self.selected_num_pos = []

    def redraw(self):
        """
        uses window reference to fill screen with black then call draw_grid() to redraw the grid
        """
        self.window.fill(self.BLACK)
        self.draw_grid()

    def place(self, key):
        """
        :param key: number user entered to put into the board

        If the selected cell is not an original cell(uneditable) then insert it into the board
        """
        col, row = self.selected
        if self.original_numbers[row][col] != 1:
            self.board[row][col] = key
        self.temp = None

    def delete_pos(self):
        """
        Deletes the number at the selected position if it is not an original number(uneditable)
        """
        col, row = self.selected
        if self.original_numbers[row][col] != 1:
            self.board[row][col] = 0

    def solve_self(self):
        """
        Solves the Sudoku board using recursion and backtracking

        Backtracking description:
            Finds first vacant cells using find_vacant_cell into vacant_position
            then on that current cell for each number 1-9 check if it satisfies the rules of sudoku using
            check_position() if the rules are satisfied insert it into the board call board_changes and pygame
            display.update() to update the board set delay so that it is watch able lastly call solve_self() again
            and proceed. If the number does not satisfy the rules of Sudoku reset value back to 0.

        :return: True is board is solved or False if the board is not solvable
        """
        vacant_position = find_vacant_cell(self.board)
        if vacant_position[0] == -1:
            return True
        row = vacant_position[0]
        col = vacant_position[1]
        for i in range(1, 10):
            if check_position(i, row, col, self.board):
                self.board[row][col] = i
                self.board_changes(row, col, True)
                pygame.display.update()
                pygame.time.delay(100)

                if self.solve_self():
                    return True

                self.board[row][col] = 0
                self.board_changes(row, col, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False

    def board_changes(self, row, col, correct=True):
        """
        :param row: selected row
        :param col: selected col
        :param correct: True if the number satisfies the rules False if backtracking

        Used only in self_solve() to show the algorithm at work

        Draws a green or red square depending on correct param. Draws the current number into the board
        """
        fnt = pygame.font.SysFont("comicsans", 40)

        # Draws black square to erase the previous number in the position
        pygame.draw.rect(self.window, self.BLACK,
                         (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 0)

        # Draws the number of the current col, row value
        text = fnt.render(str(self.board[row][col]), 1, self.WHITE)
        self.window.blit(text, (col * self.cell_size + (self.cell_size // 2 - text.get_width() / 2),
                                row * self.cell_size + (self.cell_size // 2 - text.get_height() / 2)))

        # If correct param is True draw green square if not draw red
        if correct:
            pygame.draw.rect(self.window, (0, 255, 0),
                             (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 3)
        else:
            pygame.draw.rect(self.window, (255, 0, 0),
                             (col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size), 3)

    def guess(self, key):
        """
        :param key: number key hit by user

        Used to draw grey numbers into the to add response to number key strikes by user
        called when user does a number key stroke but does not hit entere
        sets the temp variable to the key struck to be drawn in by draw_grid() function
        """
        col, row = self.selected
        if self.original_numbers[row][col] != 1:
            self.temp = key

    def check_board(self):
        """
        Checks the board against the solution. Selects the position of all cells with incorrect numbers entered by the
        user
        """
        self.selected_num_pos = []
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != self.solved_board[row][col] and self.board[row][col] != 0:
                    self.selected_num_pos.append((col, row))

    def isOver(self):
        """
        Checks the board against the solution
        :return: True if game is solved correctly, False if not
        """
        if self.solved_board == self.board:
            return True
        else:
            return False
