import time
from flask import Flask, jsonify
from game_registry import GameRegistry
from game import TicTocGame


app = Flask(__name__)
start_time = int(time.time())
store = GameRegistry()


@app.errorhandler(Exception)
def handle_exception(e):
    """
    log exception and return 503
    """
    app.logger.error(e)
    return "Service Unavailable", 503


@app.route("/game", methods=["POST"])
def create_game():
    """
    POST /game
    """
    game = TicTocGame()
    store.save_game(game)
    return jsonify(id=game.id, turnCount=game.turnCount, status=game.status.value), 201


@app.route("/game/<id>", methods=["GET"])
def get_game(id: str):
    """
    GET /game/{id}
    """
    if not store.is_game_exist(id):
        return "Not found (game does not exist)", 404
    game = store.load_game(id)
    return jsonify(id=game.id, turnCount=game.turnCount, status=game.status.value)


@app.route("/game/<id>/<int:board_position>", methods=["GET"])
def get_game_board_position(id: str, board_position: int):
    """
    GET /game/<id>/<board_position>
    """
    if board_position < 0 or board_position > 8:
        return jsonify(error="invalid board position"), 400
    if not store.is_game_exist(id):
        return "Not found (game does not exist)", 404
    game = store.load_game(id)
    return jsonify(
        gameId=game.id,
        boardPosition=board_position,
        value=game.get_position_value(board_position).value,
    )


@app.route("/game/<id>/<int:board_position>", methods=["PATCH"])
def play_game(id: str, board_position: int):
    """
    PATCH /game/<id>/<board_position>
    """
    if board_position < 0 or board_position > 8:
        return jsonify(error="invalid board position"), 400
    if not store.is_game_exist(id):
        return "Not found (game does not exist)", 404
    game = store.load_game(id)
    if not game.is_game_active():
        return jsonify(error="game not active"), 400
    if not game.is_position_empty(board_position):
        return jsonify(error="board position occupied"), 400
    game.move(board_position)
    store.save_game(game)
    return jsonify(gameId=game.id, boardPosition=board_position, value="x")


@app.route("/health", methods=["GET"])
def get_health():
    """
    GET /health
    """
    return jsonify(uptime=int(time.time()) - start_time)
