from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
from typing import Optional, List
import logging
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class PieceError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Piece(ABC):
    icon: str
    value: Optional[int]
    color: str
    symbol: str


    def __init__(self, icon: str, symbol: str, value: int, color: str) -> None:
        self.icon = icon
        self.symbol = symbol
        self.value = value
        self.color = color

    @abstractmethod
    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        """ Returns whether the piece can move to a new position. """
        pass

    def __repr__(self) -> str:
        return str(self)
    def __str__(self) -> str:
        s = ""
        if self.color == "Black":
            s += Style.BRIGHT + Fore.BLACK
        else:
            s += Style.BRIGHT + Fore.WHITE
        return s + self.icon + Style.NORMAL + Fore.RESET

class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♟︎", "p", 1, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        if board[new_position[0]][new_position[1]] is not None and board[new_position[0]][new_position[1]].color == self.color:
            return False
        direction = 1 if self.color == "Black" else -1
        row_difference = (new_position[0] - position[0]) * direction
        column_difference = abs(new_position[1] - position[1])
        if row_difference == 1 and column_difference == 0 and board[new_position[0]][new_position[1]] is None:
            return True
        if row_difference == 2 and column_difference == 0 and board[new_position[0]][new_position[1]] is None and position[0] == (1 if direction > 0 else 6):
            return True
        elif row_difference == 1 and column_difference == 1 and board[new_position[0]][new_position[1]] is not None:
            return True
        return False

class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♞", "n", 3, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        if board[new_position[0]][new_position[1]] is not None and board[new_position[0]][new_position[1]].color == self.color:
            return False
        row_difference = abs(new_position[0] - position[0])
        column_difference = abs(new_position[1] - position[1])
        if row_difference + column_difference == 3 and row_difference != 0 and column_difference != 0:
            return True
        return False

class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♝", "b", 3, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        if board[new_position[0]][new_position[1]] is not None and board[new_position[0]][new_position[1]].color == self.color:
            return False
        minimum_row = min(new_position[0], position[0])
        maximum_row = max(new_position[0], position[0])
        row_direction = 1 if new_position[0] > position[0] else -1
        minimum_column = min(new_position[1], position[1])
        maximum_column = max(new_position[1], position[1])
        column_direction = 1 if new_position[1] > position[1] else -1
        if maximum_row - minimum_row == maximum_column - minimum_column:
            for row, column in zip(range(minimum_row + 1, maximum_row)[::row_direction], range(minimum_column + 1, maximum_column)[::column_direction]):
                if board[row][column] is not None:
                    return False
            return True
        return False

class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♜", "r", 5, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        if board[new_position[0]][new_position[1]] is not None and board[new_position[0]][new_position[1]].color == self.color:
            return False
        if new_position[0] == position[0]:
            row = new_position[0]
            minimum = min(new_position[1], position[1])
            maximum = max(new_position[1], position[1])
            for column in range(minimum + 1, maximum):
                if board[row][column] is not None:
                    return False
            return True
        elif new_position[1] == position[1]:
            column = new_position[1]
            minimum = min(new_position[0], position[0])
            maximum = max(new_position[0], position[0])
            for row in range(minimum + 1, maximum):
                if board[row][column] is not None:
                    return False
            return True
        return False

class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♛", "q", 9, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        return Rook.is_move_legal(self, board, position, new_position) or Bishop.is_move_legal(self, board, position, new_position)

class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__("♚", "k", None, color)

    def is_move_legal(self, board: List[List[Optional[Piece]]], position: List[int], new_position: List[int]) -> bool:
        if board[new_position[0]][new_position[1]] is not None and board[new_position[0]][new_position[1]].color == self.color:
            return False
        row_difference = abs(new_position[0] - position[0])
        column_difference = abs(new_position[1] - position[1])
        if row_difference <= 1 and column_difference <= 1:
            return True
        return False
