from flask import Blueprint, request, abort
import json
from twitch import get_user
import gameData
import random
import time


widget_endpoint = Blueprint('widget_endpoint', __name__)


@widget_endpoint.route('/ratmaze/userdata/<user_id>')
def userdata(user_id):
    user = get_user(user_id)

    json_dict = {}
    game_dict = {}

    temp_mock_game()

    game_dict["directions"] = gameData.directions.__dict__
    game_dict["next_turn"] = gameData.next_turn
    game_dict["shop"] = list([item.to_dict() for item in gameData.shop])

    json_dict["user"] = user.__dict__
    json_dict["game"] = game_dict
    return json.dumps(json_dict)


@widget_endpoint.route('/ratmaze/vote', methods=['POST'])
def vote():
    user_id = request.args.get("id", type=int)
    direction = request.args.get("direction")

    user = get_user(user_id)
    if all(user.id not in lst for lst in gameData.votes.values()):
        match direction:
            case "up":
                if gameData.directions.up:
                    gameData.votes["up"].append(user.id)
                else:
                    abort(400)
                    return
            case "right":
                if gameData.directions.right:
                    gameData.votes["right"].append(user.id)
                else:
                    abort(400)
                    return
            case "down":
                if gameData.directions.down:
                    gameData.votes["down"].append(user.id)
                else:
                    abort(400)
                    return
            case "left":
                if gameData.directions.left:
                    gameData.votes["left"].append(user.id)
                else:
                    abort(400)
                    return
        return {"message": "Submitted successfully."}
    else:
        abort(400)


@widget_endpoint.route('/ratmaze/buy', methods=['POST'])
def buy():
    user_id = request.args.get("id", type=int)
    item_id = request.args.get("item", type=int)

    user = get_user(user_id)
    item = next((i for i in gameData.shop if i.id == item_id), None)
    if item is not None:
        if user.balance >= item.cost:
            if not (item.total_stock > 0 and item.current_stock <= 0):
                if item.total_stock > 0:
                    item.current_stock -= 1
                user.balance -= item.cost
                user.update()
                return {"message": "Purchased successfully."}

    abort(400)


def temp_mock_game():
    if int(time.time()) > gameData.next_turn:
        gameData.directions.up = random.choice([True, False])
        gameData.directions.left = random.choice([True, False])
        gameData.directions.right = random.choice([True, False])
        gameData.directions.down = random.choice([True, False])
        # gameData.reset_shop()
    gameData.handle_votes()

