import sqlite3
import os
import random
import time
import threading
from enum import Enum


class Rarity(Enum):
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    LEGENDARY = 4

    def __str__(self):
        return self.name

    def to_json(self):
        return self.name

    @classmethod
    def from_json(cls, data):
        return cls[data]


class Direction(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

    def from_str(value):
        try:
            return Direction(value)
        except ValueError:
            return None

    def to_str(self):
        return self.value

    @classmethod
    def from_json(cls, data):
        return cls[data]


class Item:
    def __init__(self, item):
        self.id = item[0]
        self.name = item[1]
        self.description = item[2]
        self.cost = item[3]
        self.total_stock = item[4]
        self.current_stock = item[4]
        self.excluded = item[5]
        self.rarity = Rarity(item[6])
        self.family = item[7]

        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM ItemConfigs WHERE ItemId = ?", (item[0],))
        config = {c[1]: c[2] for c in cursor.fetchall()}
        self.config = config

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "cost": self.cost,
            "current_stock": self.current_stock,
            "total_stock": self.total_stock,
            "rarity": self.rarity.name.title(),
        }


class GameData:
    def __init__(self, user_manager, debug=False):
        self.user_manager = user_manager
        self.debug = debug
        self.directions = {
            Direction.UP: False,
            Direction.RIGHT: False,
            Direction.DOWN: False,
            Direction.LEFT: False
        }
        self.next_turn = 0
        self.votes = {}
        self.shop = []
        self.winning_vote = None
        self.live_event = threading.Event()
        self.can_vote_event = threading.Event()
        self.leaderboard = []
        self.cheese_count = 0
        self.cheese_worthy = []

        self.threshold = 2  # TODO: DB value
        self.inc = 1  # TODO: DB value
        self.turn_len = 3  # TODO: DB value
        self.shop_size = 5  # TODO: DB value
        self.leaderboard_size = 5  # TODO: DB value
        self.cheese_points = 20  # TODO: DBvalue
        self.offline_leaderboard_size = 10

        self.offline_leaderboard = self.user_manager.get_top_users(self.offline_leaderboard_size, True)
        self.item_rarities = {
            Rarity.COMMON: 0.6,
            Rarity.UNCOMMON: 0.25,
            Rarity.RARE: 0.1,
            Rarity.LEGENDARY: 0.05
        }  # TODO: DB value

    def start_game(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        cursor.execute("UPDATE Users SET Balance=0, CurrentPoints=0;")
        connection.commit()
        self.user_manager.refresh_users()
        self.reset_votes()
        self.reset_shop()
        self.live_event.set()
        self.cheese_worthy = []
        self.cheese_count = 0
        self.user_manager.clear_cheese()

    def end_game(self):
        self.reset_votes()
        self.shop = []
        self.next_turn = 0
        self.live_event.clear()
        self.can_vote_event.clear()
        self.cheese_worthy = []
        self.offline_leaderboard = self.user_manager.get_top_users(self.offline_leaderboard_size, True)

    def reset_votes(self):
        self.votes[Direction.UP] = []
        self.votes[Direction.RIGHT] = []
        self.votes[Direction.DOWN] = []
        self.votes[Direction.LEFT] = []

    def reset_shop(self):
        self.shop = []
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Items")
        data = cursor.fetchall()
        items = {}
        used_families = []
        used_items = []
        for entry in data:
            item = Item(entry)
            items.setdefault(item.rarity, []).append(item)

        rarities = list(self.item_rarities.keys())
        weights = list(self.item_rarities.values())

        while len(self.shop) < self.shop_size:
            rarity = random.choices(rarities, weights=weights, k=1)[0]
            options = [
                item for item in items[rarity]
                if item.family not in used_families and item.name not in used_items
            ]

            if len(options) == 0:
                continue

            item = random.choice(options)
            self.shop.append(item)
            if item.family is not None:
                used_families.append(item.family)
            used_items.append(item.name)

    def get_random_item(self):
        connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Items WHERE NOT RandomExcluded")
        items = cursor.fetchall()
        item = random.choice(items)
        return Item(item)

    def can_vote(self, user):
        return all(user not in lst for lst in self.votes.values()) and self.can_vote_event.is_set()

    def award_points(self, cheese=False):
        is_empty = all(not lst for lst in self.votes.values())
        if not is_empty:
            for user in self.votes[self.winning_vote]:
                user.award_points(self.inc)
            self.reset_votes()
        if cheese:
            self.cheese_count += 1
            for user in self.cheese_worthy:
                user.award_points(self.cheese_points, award_cheese=True)
            self.cheese_worthy = []
        # refresh our leaderboard
        self.leaderboard = self.user_manager.get_top_users(self.leaderboard_size)

    def end_vote(self, direction):
        if direction is not None:
            self.can_vote_event.clear()
            self.winning_vote = direction
        elif self.can_vote_event.is_set():
            self.update_end_time()

    def start_vote(self):
        self.update_end_time()
        self.can_vote_event.set()
        self.winning_vote = None

    def handle_votes(self):
        for direction, users in self.votes.items():
            if len(users) > self.threshold:
                self.end_vote(direction)

    def cast_vote(self, user, direction):
        if self.can_vote(user):
            self.votes[direction].append(user)
            if user not in self.cheese_worthy:
                self.cheese_worthy.append(user)
            self.handle_votes()

    def get_top_direction(self):
        options = {}
        for direction in self.votes:
            count = len(self.votes[direction])
            if count > 0:
                if count not in options:
                    options[count] = []
                options[count].append(direction)
        if len(options) == 0:
            return None

        sorted_groups = sorted(options.items(), key=lambda item: item[0], reverse=True)
        return random.choice(sorted_groups[0][1])

    def update_end_time(self):
        curr_time = int(time.time())
        self.next_turn = curr_time + self.turn_len
