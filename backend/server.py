import eventlet
eventlet.monkey_patch()
from flask import Flask
from socket_handler import SocketHandler
from game_data import GameData
from user_manager import UserManager
from api import api_endpoint
import time
import argparse

app = Flask(__name__)
app.register_blueprint(api_endpoint)


def timer_thread(game, sock):
    prev_time = 0
    while True:
        game.live_event.wait()
        while game.live_event.is_set():
            # Did not hit vote threshold
            if game.next_turn >= prev_time and game.can_vote_event.is_set():
                game.end_vote(game.get_top_direction())
                sock.send_update_to_all_users()
                game.update_end_time()
                # Votes were cast
                if not game.can_vote_event.is_set():
                    sock.send_vote_to_game(game.winning_vote)
                    game.can_vote_event.wait()
                else:
                    sock.send_update_to_game()

            curr_time = int(time.time())
            socketio.sleep(max(game.next_turn - curr_time, game.turn_len))


dev = False
debug = False

# Only happens when we call from commandline
if __name__ == "__main__":
    dev = True
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        debug = True


user_manager = UserManager()
game_data = GameData(user_manager, debug)
socket_handler = SocketHandler(app, game_data, user_manager, dev)
socketio = socket_handler.socket
socketio.start_background_task(target=timer_thread, game=game_data, sock=socket_handler)
if __name__ == "__main__":
    socket_handler.run()
