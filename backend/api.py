from flask import Blueprint
import sqlite3
import os

api_endpoint = Blueprint('api_endpoint', __name__)


@api_endpoint.route('/api/config')
def config():
    connection = sqlite3.connect(os.getenv('RATMAZE_DB'))
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM Config")
    configs = cursor.fetchall()
    formatted_configs = {}
    for conf in configs:
        formatted_configs[conf[0]] = {
            "name": conf[1],
            "value": conf[2],
            "description": conf[3]
        }

    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    formatted_items = {}
    for item in items:
        formatted_items[item[0]] = {
            "name": item[1],
            "description": item[2],
            "cost": item[3],
            "stock": item[4],
            "in_random": not item[5],
            "rarity": item[6],
            "family": item[7] if item[7] is not None else ""
        }

    cursor.execute("SELECT * FROM ItemRarities")
    rarities = cursor.fetchall()
    formatted_rarities = {}
    for rarity in rarities:
        formatted_rarities[int(rarity[0])] = {
            "name": rarity[1],
            "percent": rarity[2]
        }

    return {
        "configs": formatted_configs,
        "items": formatted_items,
        "item_rarities": formatted_rarities
    }
