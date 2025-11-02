from flask import Flask
from widget import widget_endpoint
import sys
import gameData

app = Flask(__name__)
app.register_blueprint(widget_endpoint)


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    gameData.start_game()
    if len(sys.argv) > 1 and sys.argv[1] == "debug":
        app.run(debug=True)
    else:
        app.run(debug=False)
