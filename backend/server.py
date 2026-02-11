from flask import Flask
from socket_handler import SocketHandler
from game_data import GameData
from user_manager import UserManager
import threading
import time
import argparse
import os

app = Flask(__name__)
lock = threading.Lock()


def timer_thread(game, sock):
    prev_time = 0
    while True:
        game.live_event.wait()
        while game.live_event.is_set():
            with lock:
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
            time.sleep(max(game.next_turn - curr_time, game.turn_len))


debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
user_manager = UserManager()
game_data = GameData(user_manager, debug_mode)
socket_handler = SocketHandler(app, game_data, user_manager)
socketio = socket_handler.socket

thread = threading.Thread(target=timer_thread, args=(game_data, socket_handler), daemon=True)
thread.start()

if __name__ == "__main__":
    print(os.getenv('RATMAZE_DB'))
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args()
    if args.debug:
        game_data.debug = True

    socket_handler.run(args.debug)