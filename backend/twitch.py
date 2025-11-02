import sqlite3
import os
import time

import requests


class User:
    def __init__(self, id, username, balance, total_points, current_points):
        self.id = id
        self.username = username
        self.balance = balance
        self.current_points = current_points
        self.total_points = total_points

    def update(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute(f"UPDATE Users SET Username = ?, Balance = ?, TotalPoints = ?, CurrentPoints = ? WHERE Id = ?",
                       (self.username, self.balance, self.total_points, self.current_points, self.id))
        connection.commit()


def get_user(user_id):
    connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Users WHERE Id = ?", (user_id,))
    user = cursor.fetchone()
    if len(user) > 0:
        return User(user[0], user[1], user[2], user[3], user[4])

    verify_token(connection)

    cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchClientId'")
    client_id = cursor.fetchone()[0]
    cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchAccessToken'")
    access_token = cursor.fetchone()[0]

    url = "https://api.twitch.tv/helix/users"
    headers = {
        "Client-Id": client_id,
        "Authorization": f"Bearer {access_token}",
    }
    params = {
        "id": user_id
    }

    response = requests.get(url, headers=headers, params=params)
    json = response.json()
    data = json["data"][0]
    cursor.execute("INSERT INTO Users (Id, Username) VALUES(?, ?)", (data["id"], data["display_name"]))
    connection.commit()


def verify_token(connection):
    cursor = connection.cursor()
    curr_time = time.time()

    cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchAccessExpiration'")
    expiration = cursor.fetchone()

    if int(curr_time) > int(expiration[0]):
        print("Updating token!")
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchClientId'")
        client_id = cursor.fetchone()
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchClientSecret'")
        client_secret = cursor.fetchone()

        url = "https://id.twitch.tv/oauth2/token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials"
        }
        response = requests.post(url, data=data)
        json = response.json()
        access_token = json["access_token"]
        expiration = int(curr_time) + int(json["expires_in"])

        cursor.execute("UPDATE Constants SET Value = '?' WHERE Name = 'TwitchAccessToken'", (access_token,))
        cursor.execute("UPDATE Constants SET Value = '?' WHERE Name = 'TwitchAccessExpiration'", (expiration,))
        connection.commit()
