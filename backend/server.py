from flask import Flask
from socket_handler import SocketHandler
import sys
from game_data import GameData
from user_manager import UserManager
import threading
import time

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


if __name__ == "__main__":
    user_manager = UserManager()
    game_data = GameData(user_manager)
    socket = SocketHandler(app, game_data, user_manager)
    thread = threading.Thread(target=timer_thread, args=(game_data, socket))
    thread.start()
    socket.run(len(sys.argv) > 1 and sys.argv[1] == "debug")
