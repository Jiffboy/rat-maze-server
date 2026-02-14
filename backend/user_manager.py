import sqlite3
import os
import time
import random
import base64
import jwt
from adjectives import adjectives

import requests


class User:
    def __init__(self, id, twitch_id, username, balance, total_points, current_points, total_cheese):
        self.id = id
        self.twitch_id = twitch_id
        self.username = username
        self.balance = balance
        self.current_points = current_points
        self.total_points = total_points
        self.total_cheese = total_cheese

    def update(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute(f"UPDATE Users SET TwitchId = ?, Username = ?, Balance = ?, TotalPoints = ?, CurrentPoints = ?, TotalCheese = ? WHERE Id = ?",
                       (self.twitch_id, self.username, self.balance, self.total_points, self.current_points, self.total_cheese, self.id))
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

        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchClientId'")
        self.client_id = cursor.fetchone()[0]
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchClientSecret'")
        self.client_secret = cursor.fetchone()[0]
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchAccessToken'")
        self.access_token = cursor.fetchone()[0]
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchAccessExpiration'")
        self.expiration = cursor.fetchone()[0]
        cursor.execute("SELECT Value FROM Constants WHERE Name = 'TwitchExtensionSecret'")
        self.extension_secret = cursor.fetchone()[0]

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
        if user_id in self.id_map:
            return self.id_map[user_id]
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM Users WHERE Id = ?", (user_id,))
        user = cursor.fetchone()
        if user is not None and len(user) > 0:
            user = User(user[0], user[1], user[2], user[3], user[4], user[5], user[6])
            self.id_map[user_id] = user
            return user
        return None

    def get_user_from_jwt(self, token):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        decoded_secret = base64.b64decode(self.extension_secret)
        try:
            decoded = jwt.decode(token, decoded_secret, algorithms=["HS256"])
            user_id = decoded['opaque_user_id']
            user = self.get_user(user_id)

            if user is None:
                if 'user_id' in decoded:
                    twitch_id = decoded['user_id']
                    name = self.get_twitch_username(twitch_id)
                    cursor.execute("INSERT INTO Users (Id, TwitchId, Username) VALUES(?, ?, ?)", (user_id, twitch_id, name))
                else:
                    # We do not have access to their username, so we give them an anonymous alias
                    name = self.get_random_name()
                    cursor.execute("INSERT INTO Users (Id, Username) VALUES(?, ?)", (user_id, name))
                connection.commit()
                return self.get_user(user_id)

            else:
                # If someone was previously anonymous, we can update them to use their name
                if 'user_id' in decoded and user.twitch_id == 0:
                    user.twitch_id = decoded['user_id']
                    user.username = self.get_twitch_username(user.twitch_id)
                    user.update()
                return user

        except jwt.InvalidTokenError:
            return None

    def get_twitch_username(self, user_id):
        self.verify_token()
        url = "https://api.twitch.tv/helix/users"
        headers = {
            "Client-Id": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }
        params = {
            "id": str(user_id)
        }

        response = requests.get(url, headers=headers, params=params)
        json = response.json()
        data = json["data"][0]
        return data["display_name"]

    def verify_token(self):
        curr_time = time.time()

        if int(curr_time) > int(self.expiration):
            url = "https://id.twitch.tv/oauth2/token"
            data = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }
            response = requests.post(url, data=data)
            json = response.json()
            self.access_token = json["access_token"]
            self.expiration = int(curr_time) + int(json["expires_in"])

            connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
            cursor = connection.cursor()
            cursor.execute("UPDATE Constants SET Value = ? WHERE Name = 'TwitchAccessToken'", (self.access_token,))
            cursor.execute("UPDATE Constants SET Value = ? WHERE Name = 'TwitchAccessExpiration'", (self.expiration,))
            connection.commit()

    def get_random_name(self):
        return f"{random.choice(adjectives)} Rat"
