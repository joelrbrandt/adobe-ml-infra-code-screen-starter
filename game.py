from typing import Optional, List
from enum import Enum
import string
import random


class BoardValue(Enum):
    """
    values in a game board
    """

    X = "x"
    O = "o"
    EMPTY = "empty"


class GameStatus(Enum):
    """
    game status
    """

    ACTIVE = "active"
    WINNER_X = "winner_x"
    WINNER_O = "winner_o"
    DRAW = "draw"


class TicTocGame(object):
    def __init__(
        self, id: Optional[int] = None, board: Optional[List[BoardValue]] = None
    ) -> None:
        """
        create or load game
        """
        if board and id:
            self.board = board
            self.id = id
        else:
            self.create_game()

    def create_game(self) -> None:
        """
        setup a new game
        """
        self.board = [BoardValue.EMPTY] * 9
        self.id = self.generate_game_id()
        return

    def generate_game_id(self, length: int = 6) -> str:
        """
        generate a random alphanumeric string with length
        """
        return "".join(
            random.choice(
                string.ascii_uppercase + string.ascii_lowercase + string.digits
            )
            for _ in range(length)
        )

    def is_winner(self, player: BoardValue) -> bool:
        """
        check if a player is the winner
        """
        return (
            # row
            (
                (
                    self.board[0] == player
                    and self.board[1] == player
                    and self.board[2] == player
                )
                or (
                    self.board[3] == player
                    and self.board[4] == player
                    and self.board[5] == player
                )
                or (
                    self.board[6] == player
                    and self.board[7] == player
                    and self.board[8] == player
                )
            )
            # col
            or (
                (
                    self.board[0] == player
                    and self.board[3] == player
                    and self.board[6] == player
                )
                or (
                    self.board[1] == player
                    and self.board[4] == player
                    and self.board[7] == player
                )
                or (
                    self.board[2] == player
                    and self.board[5] == player
                    and self.board[8] == player
                )
            )
            # diag
            or (
                self.board[0] == player
                and self.board[4] == player
                and self.board[8] == player
            )
            or (
                self.board[2] == player
                and self.board[4] == player
                and self.board[6] == player
            )
        )

    @property
    def status(self) -> GameStatus:
        """
        active, winner-x, winner-o, draw
        """
        if self.is_winner(BoardValue.O):
            return GameStatus.WINNER_O
        if self.is_winner(BoardValue.X):
            return GameStatus.WINNER_X
        if self.turnCount == 9:
            return GameStatus.DRAW
        return GameStatus.ACTIVE

    @property
    def turnCount(self) -> int:
        """
        turn count equals to non-empty values in the board
        """
        turnCount = 0
        for value in self.board:
            turnCount += value != BoardValue.EMPTY
        return turnCount

    def is_position_valid(self, position: int) -> bool:
        """
        0 <= position < 9?
        """
        return position >= 0 and position < 9

    def is_position_empty(self, position: int) -> bool:
        """
        value == empty?
        """
        return self.board[position] == BoardValue.EMPTY

    def is_game_active(self) -> bool:
        """
        game status == active?
        """
        return self.status == GameStatus.ACTIVE

    def get_position_value(self, position: int) -> BoardValue:
        """
        get value in the board
        """
        if not self.is_position_valid(position):
            raise ValueError("invalid board position")
        return self.board[position]

    def set_position_value(self, position: int, value: BoardValue) -> None:
        """
        set value in the board
        """
        if not self.is_position_valid(position):
            raise ValueError("invalid board position")
        if not self.is_position_empty(position):
            raise ValueError("board position occupied")
        self.board[position] = value
        return

    def move(self, position: int) -> None:
        """
        player X makes a move, then O makes a move
        """
        if not self.is_game_active():
            raise ValueError("game not active")
        # move X
        self.set_position_value(position, BoardValue.X)
        # computer only moves when game is still active
        if self.is_game_active():
            # computer makes a valid random move
            possible_move_index = []
            for index in range(0, len(self.board)):
                if self.is_position_empty(index):
                    possible_move_index.append(index)
            self.set_position_value(random.choice(possible_move_index), BoardValue.O)
