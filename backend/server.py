from flask import Flask
from socket_def import socketio
from widget import widget_endpoint
import sys
import gameData
import threading
import random
import time

app = Flask(__name__)
app.register_blueprint(widget_endpoint)

socketio.init_app(app)
lock = threading.Lock()

# Must be imported after socketio instantiated. Cursed but whatever
import widget


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# THIS IS TEMPORARY MAKE SURE TO REMOVE
def temp_mock_game():
    gameData.directions[gameData.Direction.UP] = random.choice([True, False])
    gameData.directions[gameData.Direction.RIGHT] = random.choice([True, False])
    gameData.directions[gameData.Direction.DOWN] = random.choice([True, False])
    gameData.directions[gameData.Direction.LEFT] = random.choice([True, False])
    # gameData.reset_shop()


def timer_thread():
    prev_time = 0
    while True:
        with lock:
            # Did not hit vote threshold
            if gameData.next_turn >= prev_time:
                gameData.end_vote(gameData.Direction.RIGHT)
            prev_time = gameData.next_turn
            temp_mock_game()
            widget.update_all()
        curr_time = int(time.time())
        time.sleep(max(gameData.next_turn - curr_time, gameData.turn_len))


if __name__ == "__main__":
    gameData.start_game()
    thread = threading.Thread(target=timer_thread)
    thread.start()
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        socketio.run(app, debug=True)
    else:
        socketio.run(app, debug=False, allow_unsafe_werkzeug=True)
