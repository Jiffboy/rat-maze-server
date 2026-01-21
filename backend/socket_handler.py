from flask_socketio import SocketIO
from flask import request
from twitch import get_user
from game_data import Direction


class SocketHandler:
    def __init__(self, app, game_data):
        # TODO: Add disconnect! Remove from map
        # TODO: Add encryption for streamer login
        # TODO: Figure out user encryption? Maybe we get a token from twitch in api. Look into this.
        self.socket = SocketIO(cors_allowed_origins="*")
        self.socket.init_app(app)
        self.app = app
        self.user_sid_map = {}
        self.game_sid = 0
        self.game_data = game_data

        # WIDGET EVENTS
        @self.socket.on("connect", namespace="/ratmaze/widget")
        def on_connect(auth):
            if request.sid not in self.user_sid_map:
                self.user_sid_map[request.sid] = auth['id']
            user = get_user(auth['id'])
            self.send_update_to_user(user, request.sid)

        @self.socket.on("vote", namespace="/ratmaze/widget")
        def vote(data):
            user_id = self.user_sid_map[request.sid]
            direction = Direction.from_str(data['direction'])
            if direction is not None:
                user = get_user(user_id)

                if self.game_data.can_vote(user):
                    self.game_data.cast_vote(user, direction)
                    if not self.game_data.can_vote_event.is_set():
                        self.send_update_to_all_users()
                        self.send_vote_to_game(direction)
                    else:
                        self.send_update_to_user(user, request.sid)
                        self.send_update_to_game()

        @self.socket.on("buy", namespace="/ratmaze/widget")
        def buy(data):
            user_id = self.user_sid_map[request.sid]
            item_id = data['item']

            user = get_user(user_id)
            item = next((i for i in self.game_data.shop if i.id == item_id), None)
            if item is not None:
                if user.balance >= item.cost:
                    if not (item.total_stock > 0 >= item.current_stock):
                        if item.total_stock > 0:
                            item.current_stock -= 1
                        user.balance -= item.cost
                        user.update()
                        self.send_update_to_user(user, request.sid)
                        self.send_item_to_game(user, item)

        # GAME EVENTS
        @self.socket.on("connect", namespace="/ratmaze/game")
        def on_connect():
            self.game_sid = request.sid
            self.game_data.start_game()
            self.update_everything()

        @self.socket.on("disconnect", namespace="/ratmaze/game")
        def on_disconnect():
            self.game_sid = 0
            self.game_data.end_game()
            self.send_update_to_all_users()

        @self.socket.on("start_round", namespace="/ratmaze/game")
        def start_round(data):
            self.game_data.directions[Direction.UP] = data['directions']['up']
            self.game_data.directions[Direction.RIGHT] = data['directions']['right']
            self.game_data.directions[Direction.DOWN] = data['directions']['down']
            self.game_data.directions[Direction.LEFT] = data['directions']['left']
            self.game_data.award_points(data['got_cheese'])
            if data['got_cheese']:
                self.game_data.reset_shop()
            self.game_data.start_vote()
            self.update_everything()

        @self.socket.on("update_directions", namespace="/ratmaze/game")
        def update_directions(data):
            self.game_data.directions[Direction.UP] = data['up']
            self.game_data.directions[Direction.RIGHT] = data['right']
            self.game_data.directions[Direction.DOWN] = data['down']
            self.game_data.directions[Direction.LEFT] = data['left']
            self.send_update_to_all_users()

    def run(self, debug):
        if debug:
            self.socket.run(self.app, debug=True)
        else:
            self.socket.run(self.app, debug=False, allow_unsafe_werkzeug=True)

    def send_update_to_all_users(self):
        for sid, user_id in self.user_sid_map.items():
            user = get_user(user_id)
            self.send_update_to_user(user, sid)

    def send_update_to_user(self, user, sid):
        data = {
            "user": user.__dict__,
            "game": {
                "is_live": self.game_data.live_event.is_set(),
                "directions": {key.to_str(): value for key, value in self.game_data.directions.items()},
                "next_turn": self.game_data.next_turn,
                "can_vote": self.game_data.can_vote(user),
                "shop": list([item.to_dict() for item in self.game_data.shop])
            }
        }
        self.socket.emit("data_update", data, to=sid, namespace="/ratmaze/widget")

    def send_vote_to_game(self, direction):
        self.socket.emit("move", direction.to_str(), to=self.game_sid, namespace="/ratmaze/game")

    def send_item_to_game(self, user, item):
        data = {
            "user": user.username,
            "item": item.name,
            "config": {}
        }
        self.socket.emit("use_item", data, to=self.game_sid, namespace="/ratmaze/game")

    def send_update_to_game(self):
        data = {
            "next_turn": self.game_data.next_turn,
            "votes": {key.to_str(): len(value) for key, value in self.game_data.votes.items()},
            "leaderboard": [
                {"username": user.username, "points": user.current_points}
                for user in self.game_data.leaderboard
            ],
            "cheese_count": self.game_data.cheese_count
        }
        self.socket.emit("update", data, to=self.game_sid, namespace="/ratmaze/game")

    def update_everything(self):
        self.send_update_to_all_users()
        self.send_update_to_game()
