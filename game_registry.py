from typing import List
from game import TicTocGame, BoardValue


class GameRegistry(object):
    """
    Interface for game store
    """

    def __init__(self):
        self.registry = {}

    def is_game_exist(self, id: str) -> bool:
        """
        check if a game id exists
        """
        return id in self.registry

    def get_game(self, id: str) -> List[BoardValue]:
        """
        get game board from registry
        """
        if not self.is_game_exist(id):
            raise ValueError("Game {} does not exist in the registry".format(id))
        return self.registry[id]

    def load_game(self, id: str) -> TicTocGame:
        """
        load the game from game registry
        """
        board = self.get_game(id)
        return TicTocGame(id, board)

    def save_game(self, game: TicTocGame) -> None:
        """
        save the board to game registry
        """
        print("Create/update game {}".format(game.id))
        self.registry[game.id] = game.board
