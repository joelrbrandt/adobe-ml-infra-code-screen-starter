from unittest import TestCase
from game import TicTocGame, BoardValue, GameStatus


id = "abc123"
test_board_cases = [
    {
        "board": [
            BoardValue.X,
            BoardValue.X,
            BoardValue.X,
            BoardValue.O,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
        ],
        "turnCount": 5,
        "status": GameStatus.WINNER_X,
    },
    {
        "board": [
            BoardValue.X,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.X,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.X,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
        ],
        "turnCount": 5,
        "status": GameStatus.WINNER_X,
    },
    {
        "board": [
            BoardValue.X,
            BoardValue.X,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.X,
        ],
        "turnCount": 6,
        "status": GameStatus.WINNER_O,
    },
    {
        "board": [
            BoardValue.X,
            BoardValue.O,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
            BoardValue.EMPTY,
        ],
        "turnCount": 2,
        "status": GameStatus.ACTIVE,
    },
    {
        "board": [
            BoardValue.X,
            BoardValue.O,
            BoardValue.X,
            BoardValue.X,
            BoardValue.O,
            BoardValue.O,
            BoardValue.O,
            BoardValue.X,
            BoardValue.X,
        ],
        "turnCount": 9,
        "status": GameStatus.DRAW,
    },
]


class TestTicTacToeGame(TestCase):
    def test_create_game(self):
        """
        test a valid game can be created
        """
        game = TicTocGame()
        self.assertIsNotNone(game.id)
        self.assertIsNotNone(game.board)
        self.assertEqual(len(game.id), 6)
        self.assertEqual(len(game.board), 9)
        self.assertEqual(game.status, GameStatus.ACTIVE)
        self.assertEqual(game.turnCount, 0)

    def test_game_results(self):
        """
        test game result is correct
        """
        for test_board in test_board_cases:
            game = TicTocGame(id, test_board["board"])
            self.assertEqual(game.status, test_board["status"])
            self.assertEqual(game.turnCount, test_board["turnCount"])

    def test_raise_error_when_position_is_not_valid(self):
        """
        test invalid board position
        """
        game = TicTocGame()
        with self.assertRaises(ValueError):
            game.set_position_value(10, BoardValue.O)

    def test_raise_error_when_position_is_not_empty(self):
        """
        test board position occupied
        """
        game = TicTocGame()
        game.set_position_value(0, BoardValue.O)
        with self.assertRaises(ValueError):
            game.set_position_value(0, BoardValue.X)

    def test_not_move_when_game_is_not_active(self):
        """
        test game not active
        """
        game = TicTocGame(id, test_board_cases[0]["board"])
        with self.assertRaises(ValueError):
            game.move(1)

    def test_computer_move(self):
        """
        test computer moves correctly
        """
        game = TicTocGame()
        game.move(0)
        self.assertEqual(game.turnCount, 2)
        self.assertEqual(game.status, GameStatus.ACTIVE)
        self.assertEqual(game.get_position_value(0), BoardValue.X)
        self.assertTrue(BoardValue.O in game.board)
