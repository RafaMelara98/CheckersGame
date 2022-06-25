import pygame
from checkers.Variables import NEGRO, ROWS, ROJO, SQUARE, COLUMNS, BLANCO
from checkers.Pieza import Pieza

class Tablero:
    def __init__(self):
        self.tablero = []
        self.rojo_left = self.blanco_left = 12
        self.rojo_kings = self.blanco_kings = 0
        self.create_tablero()
    
    def draw_squares(self, win):
        win.fill(NEGRO)
        for row in range(ROWS):
            for col in range(row % 2, COLUMNS, 2):
                pygame.draw.rect(win, BLANCO, (row*SQUARE, col *SQUARE, SQUARE, SQUARE))

    def move(self, piece, row, col):
        self.tablero[piece.row][piece.col], self.tablero[row][col] = self.tablero[row][col], self.tablero[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == BLANCO:
                self.blanco_kings += 1
            else:
                self.rojo_kings += 1 

    def get_piece(self, row, col):
        return self.tablero[row][col]

    def create_tablero(self):
        for row in range(ROWS):
            self.tablero.append([])
            for col in range(COLUMNS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.tablero[row].append(Pieza(row, col, BLANCO))
                    elif row > 4:
                        self.tablero[row].append(Pieza(row, col, BLANCO))
                    else:
                        self.tablero[row].append(0)
                else:
                    self.tablero[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLUMNS):
                piece = self.tablero[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.tablero[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == ROJO:
                    self.rojo_left -= 1
                else:
                    self.blanco_left -= 1
    
    def winner(self):
        if self.rojo_left <= 0:
            return BLANCO
        elif self.blanco_left <= 0:
            return ROJO
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == ROJO or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == BLANCO or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.tablero[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLUMNS:
                break
            
            current = self.tablero[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves