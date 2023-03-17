from typing import Optional, List, Dict
from pieces import Piece, Pawn, Knight, Bishop, Rook, Queen, King
from colorama import Back, Fore, Style
import os
import logging

logger = logging.getLogger(__name__)

COLUMNS: str = "ABCDEFGH"
ROWS: str = "87654321"

class BoardError(Exception):
    def __init__(self, message):
        super().__init__(message)

def convert_position(position: str) -> List[int]:
    if position[0] not in COLUMNS or position[1] not in ROWS:
        raise BoardError(f"Invalid position: {position}")
    return [ROWS.index(position[1]), COLUMNS.index(position[0])]

class Board:
    board: List[List[Optional[Piece]]]
    size: int = 8

    def __init__(self) -> None:
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]

    def set_board(self, fen_string: str) -> None:
        """ Sets the board from a FEN string. """
        row = 0
        column = 0

        for character in fen_string:
            match character:
                case "p":
                    self.board[row][column] = Pawn("Black")
                case "n":
                    self.board[row][column] = Knight("Black")
                case "b":
                    self.board[row][column] = Bishop("Black")
                case "r":
                    self.board[row][column] = Rook("Black")
                case "q":
                    self.board[row][column] = Queen("Black")
                case "k":
                    self.board[row][column] = King("Black")
                case "P":
                    self.board[row][column] = Pawn("White")
                case "N":
                    self.board[row][column] = Knight("White")
                case "B":
                    self.board[row][column] = Bishop("White")
                case "R":
                    self.board[row][column] = Rook("White")
                case "Q":
                    self.board[row][column] = Queen("White")
                case "K":
                    self.board[row][column] = King("White")
                case "/":
                    row += 1
                    column = 0
                    continue
                case "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8":
                    column += int(character)
                    continue
                case other:
                    raise BoardError(f"Unknown character {other!r}")
            column += 1

    def get_king_position(self, color: str) -> List[int]:
        for row in range(self.size):
            for column in range(self.size):
                piece = self.board[row][column]
                if isinstance(piece, King) and piece.color == color:
                    return [row, column]
        return []

    def move(self, position_start: str, position_end: str, color) -> None:
        position_from = convert_position(position_start)
        position_to = convert_position(position_end)
        logger.debug(f"Moving from {position_start} to {position_end}")

        """ Moves a piece from position_from to position_to. """
        if position_from[0] < 0 or position_from[0] >= self.size or position_from[1] < 0 or position_from[1] >= self.size:
            raise BoardError(f"Invalid position: {position_from}")
        if position_to[0] < 0 or position_to[0] >= self.size or position_to[1] < 0 or position_to[1] >= self.size:
            raise BoardError(f"Invalid position: {position_to}")

        piece = self.board[position_from[0]][position_from[1]]
        if piece is None:
            raise BoardError(f"No piece on position: {position_from}")
        if piece.color != color:
            raise BoardError(f"Wrong color: {piece.color} expected {color}")
        if(piece.is_move_legal(self.board, position_from, position_to)):
            backup = self.board[position_to[0]][position_to[1]]
            self.board[position_from[0]][position_from[1]] = None
            self.board[position_to[0]][position_to[1]] = piece
            if self.is_attacked(self.get_king_position(color), color):
                self.board[position_to[0]][position_to[1]] = backup
                self.board[position_from[0]][position_from[1]] = piece
                raise BoardError(f"King is attacked")
        else:
            raise BoardError(f"Invalid move: {position_from} -> {position_to}")

    def is_attacked(self, position: List[int], color: str) -> bool:
        """ Checks if a position is attacked. """
        if position[0] < 0 or position[0] >= self.size or position[1] < 0 or position[1] >= self.size:
            raise BoardError(f"Invalid position: {position}")

        for row in range(self.size):
            for column in range(self.size):
                piece = self.board[row][column]
                if piece is None:
                    continue
                if piece.color != color and piece.is_move_legal(self.board, [row, column], position):
                    return True
        return False

    def is_checkmate(self, color: str) -> bool:
        for row in range(self.size):
            for column in range(self.size):
                piece = self.board[row][column]
                if piece is None or piece.color != color:
                    continue
                for row_potential in range(self.size):
                    for column_potential in range(self.size):
                        if not piece.is_move_legal(self.board, [row, column], [row_potential, column_potential]):
                            continue
                        backup = self.board[row_potential][column_potential]
                        self.board[row][column] = None
                        self.board[row_potential][column_potential] = piece
                        attacked = self.is_attacked(self.get_king_position(color), color)
                        self.board[row_potential][column_potential] = backup
                        self.board[row][column] = piece
                        if attacked:
                            continue
                        else:
                            logger.debug(f"available move {self.translate_position([row, column])} -> {self.translate_position([row_potential, column_potential])}")
                            return False
        return True

    def get_position(self) -> str:
        """ Returns the FEN representation of the board. """
        s = ""
        for row in range(self.size):
            counter = 0
            for column in range(self.size):
                piece = self.board[row][column]
                if piece is None:
                    counter += 1
                else:
                    if counter != 0:
                        s += str(counter)
                        counter = 0
                    if piece.color == "Black":
                        s += piece.symbol
                    else:
                        s += piece.symbol.upper()
            if counter != 0:
                s += str(counter)
            if row != self.size - 1:
                s += "/"
        return s

    def print(self) -> None:
        """ Prints current state of the board """
        os.system("clear")
        print(self)

    def translate_position(self, position: List[int]) -> str:
        return COLUMNS[position[1]] + ROWS[position[0]]

    def __repr__(self) -> str:
        s = "\n  "
        for column in range(self.size):
            s += " " + COLUMNS[column] + " "
        s += "\n"

        for row in range(self.size):
            s += ROWS[row] + " "
            for column in range(self.size):
                # Background color
                if (row + column) % 2 == 0:
                    s += Back.WHITE
                else:
                    s += Back.BLACK
                # Piece
                piece = self.board[row][column]
                if piece is not None:
                    s += " " + str(piece) + " "
                else:
                    s += "   "
            s += Back.RESET + "\n"

        return s
