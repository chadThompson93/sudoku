import pygame


class Button:
    """
    Simple class to create a button credit from youtube video: https://www.youtube.com/watch?v=4_9twnEduFA Tech with Tim
    """

    def __init__(self, color, x, y, width, height, text_size, text=''):
        """
        :param color: color value of the button
        :param x: x position of the button
        :param y: y position
        :param width: width of the button
        :param height: height of the button
        :param text_size: size of the text on the button
        :param text: the text to put on the button

        Initializes instance of this class and all related variable
        """
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.text_size = text_size

    def draw(self, win, outline=None):
        """
        :param win: pygame Window to draw the button
        :param outline: If you want an outline around the button set to True

        Draws the button on the screen using pygame library. Uses the classes x, y, height, width, text_size, and text
        to draw the button on the pygame window(win)
        """
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('comicsans', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
                self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        """
        :param pos: Position of the mouse cursor
        :return: True if the mouse if hovering over the button false if not

        Function used to check if the button is hovering over the button
        """
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False
