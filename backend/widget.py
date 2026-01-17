from flask import Blueprint, request
from twitch import get_user
from socket_def import socketio
import gameData


widget_endpoint = Blueprint('widget_endpoint', __name__)


# maps sid to user ids
sid_map = {}

# TODO: Add disconnect! Remove from map
# TODO: Add encryption for streamer login
# TODO: Figure out user encryption? Maybe we get a token from twitch in api. Look into this.


@socketio.on("debug_switch", namespace="/ratmaze/widget")
def switch():
    if gameData.live_event.is_set():
        gameData.end_game()
    else:
        gameData.start_game()
    user_id = sid_map[request.sid]
    user = get_user(user_id)
    send_update(user, request.sid)


@socketio.on("connect", namespace="/ratmaze/widget")
def on_connect(auth):
    if request.sid not in sid_map:
        sid_map[request.sid] = auth['id']
    user = get_user(auth['id'])
    send_update(user, request.sid)


@socketio.on("vote", namespace="/ratmaze/widget")
def vote(data):
    user_id = sid_map[request.sid]
    direction = gameData.Direction.from_str(data['direction'])
    if direction is not None:
        user = get_user(user_id)

        if gameData.can_vote(user):
            gameData.votes[direction].append(user.id)
            send_update(user, request.sid)


@socketio.on("buy", namespace="/ratmaze/widget")
def buy(data):
    user_id = sid_map[request.sid]
    item_id = data['item']

    user = get_user(user_id)
    item = next((i for i in gameData.shop if i.id == item_id), None)
    if item is not None:
        if user.balance >= item.cost:
            if not (item.total_stock > 0 >= item.current_stock):
                if item.total_stock > 0:
                    item.current_stock -= 1
                user.balance -= item.cost
                user.update()
                send_update(user, request.sid)


def update_all():
    for sid, user_id in sid_map.items():
        user = get_user(user_id)
        send_update(user, sid)


def send_update(user, sid):
    data = {
        "user": user.__dict__,
        "game": {
            "is_live": gameData.live_event.is_set(),
            "directions": {key.to_str(): value for key, value in gameData.directions.items()},
            "next_turn": gameData.next_turn,
            "can_vote": gameData.can_vote(user),
            "shop": list([item.to_dict() for item in gameData.shop])
        }
    }
    socketio.emit("data_update", data, to=sid, namespace="/ratmaze/widget")
