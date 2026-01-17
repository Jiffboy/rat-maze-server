import sqlite3
import os
from twitch import get_user
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


directions = {
    Direction.UP: False,
    Direction.RIGHT: False,
    Direction.DOWN: False,
    Direction.LEFT: False
}
next_turn = 0
votes = {}
shop = []
is_live = False
live_event = threading.Event()


threshold = 2  # TODO: DB value
inc = 1  # TODO: DB value
turn_len = 3  # TODO: DB value
shop_size = 5  # TODO: DB value

item_rarities = {
    Rarity.COMMON: 0.6,
    Rarity.UNCOMMON: 0.25,
    Rarity.RARE: 0.1,
    Rarity.LEGENDARY: 0.05
}  # TODO: DB value


def start_game():
    connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
    cursor = connection.cursor()
    cursor.execute("UPDATE Users SET Balance=0, CurrentPoints=0;")
    connection.commit()
    reset_votes()
    reset_shop()
    live_event.set()


def end_game():
    global shop
    global next_turn

    reset_votes()
    shop = []
    next_turn = 0
    live_event.clear()


def reset_votes():
    votes[Direction.UP] = []
    votes[Direction.RIGHT] = []
    votes[Direction.DOWN] = []
    votes[Direction.LEFT] = []


def reset_shop():
    global shop
    shop = []
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

    rarities = list(item_rarities.keys())
    weights = list(item_rarities.values())

    while len(shop) < shop_size:
        rarity = random.choices(rarities, weights=weights, k=1)[0]
        options = [
            item for item in items[rarity]
            if item.family not in used_families and item.name not in used_items
        ]

        if len(options) == 0:
            continue

        item = random.choice(options)
        shop.append(item)
        if item.family is not None:
            used_families.append(item.family)
        used_items.append(item.name)


def can_vote(user):
    return all(user.id not in lst for lst in votes.values())


def end_vote(direction, cheese=False):
    curr_time = int(time.time())
    global next_turn

    if direction is not None:
        for user_id in votes[direction]:
            user = get_user(user_id)
            user.balance += inc
            user.total_points += inc
            user.current_points += inc
            user.update()
    reset_votes()
    next_turn = curr_time + turn_len


def handle_votes():
    for direction, users in votes.items():
        if len(users) > threshold:
            end_vote(direction)


def get_top_direction():
    options = {}
    for direction in votes:
        count = len(votes[direction])
        if count > 0:
            if count not in options:
                options[count] = []
            options[count].append(direction)
    if len(options) == 0:
        return None

    sorted_groups = sorted(options.items(), key=lambda item: item[0], reverse=True)
    return random.choice(sorted_groups[0][1])
