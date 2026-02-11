import sqlite3
import os
import time

import requests


class User:
    def __init__(self, id, username, balance, total_points, current_points, total_cheese):
        self.id = id
        self.username = username
        self.balance = balance
        self.current_points = current_points
        self.total_points = total_points
        self.total_cheese = total_cheese

    def update(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute(f"UPDATE Users SET Username = ?, Balance = ?, TotalPoints = ?, CurrentPoints = ?, TotalCheese = ? WHERE Id = ?",
                       (self.username, self.balance, self.total_points, self.current_points, self.total_cheese, self.id))
        connection.commit()

    def refresh(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute("SELECT Balance, TotalPoints, CurrentPoints FROM Users WHERE Id = ?", (self.id,))
        user = cursor.fetchone()
        self.balance = user[0]
        self.total_points = user[1]
        self.current_points = user[2]

    def award_points(self, points, award_cheese=False):
        self.balance += points
        self.total_points += points
        self.current_points += points
        if award_cheese:
            self.total_cheese += 1
        self.update()


class UserManager:
    def __init__(self):
        # Keep these in a map so that we only have one object per user, and we only have to query SQL once
        self.id_map = {}

    def refresh_users(self):
        for user_id, user in self.id_map.items():
            user.refresh()

    def get_top_users(self, count, all_time=False):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        if all_time:
            cursor.execute("SELECT Id FROM Users Where TotalPoints > 0 ORDER BY TotalPoints DESC LIMIT ?", (count,))
        else:
            cursor.execute("SELECT Id FROM Users Where CurrentPoints > 0 ORDER BY CurrentPoints DESC LIMIT ?", (count,))
        user_ids = cursor.fetchall()
        leaderboard = []
        for user_id in user_ids:
            leaderboard.append(self.get_user(user_id[0]))
        return leaderboard

    def get_user(self, user_id):
        # Sometimes it's a string, sometimes it's not
        try:
            user_id = int(user_id)
        except Exception as e:
            print(f"Failed to parse id: {user_id}")
            return None
        if user_id in self.id_map:
            return self.id_map[user_id]
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users WHERE Id = ?", (user_id,))
        user = cursor.fetchone()
        if len(user) > 0:
            user = User(user[0], user[1], user[2], user[3], user[4], user[5])
            self.id_map[user_id] = user
            return user

        self.verify_token(connection)

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
        return self.get_user(user_id)

    def verify_token(self, connection):
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
