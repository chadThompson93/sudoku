from src import board
import pygame
import sys

from src.board import Board
from src.button import Button
from pygame.locals import *


# Set grid values
WINDOW_MULTIPLIER = 5
WINDOW_SIZE = 90
SQUARE_SIZE = (WINDOW_MULTIPLIER * WINDOW_SIZE) // 3
CELL_SIZE = SQUARE_SIZE // 3
BOTTOMGAP = 100

# Sets size of grid
WINDOW_WIDTH = WINDOW_SIZE * WINDOW_MULTIPLIER
WINDOW_HEIGHT = WINDOW_SIZE * WINDOW_MULTIPLIER

# define FPS
FPS = 10

# set background color
BLACK = (50, 50, 50)
WHITE = (255, 255, 255)
LIGHTGRAY = (100, 100, 100)

# easy board
board = [
    [7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]
]


# Medium board
# board=[[2,0,0,0,0,0,0,6,0],
#        [0,0,0,0,7,5,0,3,0],
#        [0,4,8,0,9,0,1,0,0],
#        [0,0,0,3,0,0,0,0,0],
#        [3,0,0,0,1,0,0,0,9],
#        [0,0,0,0,0,8,0,0,0],
#        [0,0,1,0,2,0,5,7,0],
#        [0,8,0,7,3,0,0,0,0],
#        [0,9,0,0,0,0,0,0,4]]

def redraw(window, board, button, window_height, bottom_gap):
    """
    :param window: reference to the game Window
    :param board: reference of the Board class
    :param window_height: Height of the Sudoku board
    :param bottom_gap: Size of the bottom part of the screen not part of Sudoku board

    Redraws the entire screen every tick of the game:
    First fills screen with BLACK then calls board.draw_grid() and the button.draw() then checks if the game is over
    if so then draw "Correct, Good Job! at the bottom of the screen"
    """
    window.fill(BLACK)
    board.draw_grid()
    button.draw(window)
    if board.isOver():
        font = pygame.font.SysFont('comicsans', 30)
        text = font.render("Correct, Good Job!", 1, (0, 255, 0))
        window.blit(text, (20, window_height+bottom_gap - 35))


def main():
    """
    Main function used to run the Sudoku game
    uses pygame functionality to track game events
    """
    # initialize pygame
    pygame.init()
    pygame.display.set_caption("Sudoku")

    # Initialize the board, check board button the game window and FPS clock and the variable holding key strokes
    global FPSCLOCK, DISPLAYSURF
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT + BOTTOMGAP))
    key = None
    sudoku_board = Board(WINDOW_WIDTH, WINDOW_HEIGHT, SQUARE_SIZE, CELL_SIZE, DISPLAYSURF, board)
    check_board = Button((LIGHTGRAY), 20, WINDOW_HEIGHT+20, 50, 25, 25,"check")

    # Fill window background with Black
    DISPLAYSURF.fill(BLACK)

    # Call board and button commands to draw initial board state
    sudoku_board.draw_grid()
    check_board.draw(DISPLAYSURF)

    # game loop watches for events such as key strokes and mouse clicks
    # redraws board and button every loop instance
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    sudoku_board.delete_pos()
                    key = None
                if event.key == pygame.K_RETURN:
                    sudoku_board.place(key)
                    key = None
                if event.key == pygame.K_SPACE:
                    sudoku_board.solve_self()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = sudoku_board.click(pos)
                if clicked:
                    sudoku_board.selected = clicked
                elif check_board.isOver(pos):
                    sudoku_board.check_board()
                key = None

            if sudoku_board.selected != (-1, -1) and key is not None:
                sudoku_board.guess(key)
        redraw(DISPLAYSURF, sudoku_board, check_board, WINDOW_HEIGHT, BOTTOMGAP)
        pygame.display.update()


if __name__ == '__main__':
    main()
