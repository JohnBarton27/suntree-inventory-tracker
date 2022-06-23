from flask import render_template

from building import Building
from item import Item
from room import Room


def index():
    num_items = len(Item.get_all())
    num_buildings = len(Building.get_all())
    num_rooms = len(Room.get_all())
    return render_template('index.html', num_items=num_items, num_buildings=num_buildings, num_rooms=num_rooms)


def scanner():
    return render_template('items/scanner.html')


def help():
    return render_template('help/help_home.html')
