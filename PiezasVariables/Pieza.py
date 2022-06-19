from .Variables import NEGRO, SQUARE, CROWN
import pygame

class Pieza:
    OUTLINE = 3
    PADDING = 5

    def init(s, row, columns, clor):
        s.row = row
        s.columns = columns
        s.clor = clor
        s.king = False
        s.x = 0
        s.y = 0
        s.calc_pos()

    def calc_pos(s):
        s.x = SQUARE * s.columns + SQUARE // 2
        s.y = SQUARE * s.row + SQUARE // 2

    def make_king(s):
        s.king = True
    
    def draw(s, win):
        radius = SQUARE//2 - s.PADDING
        pygame.draw.circle(win, NEGRO, (s.x, s.y), radius + s.OUTLINE)
        pygame.draw.circle(win, s.clor, (s.x, s.y), radius)
        if s.king:
            win.blit(CROWN, (s.x - CROWN.get_width()//2, s.y - CROWN.get_height()//2))

    def move(s, row, columns):
        s.row = row
        s.columns = columns
        s.calc_pos()

    def __repr__(s):
        return str(s.clor)