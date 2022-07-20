from flask import render_template

from building import Building
from condition import Condition
from item import Item
from room import Room


def index():
    all_items = Item.get_all()
    num_buildings = len(Building.get_all())
    num_rooms = len(Room.get_all())

    num_items = Item.get_total_num(all_items)

    poor_items = []
    fair_items = []
    good_items = []
    excellent_items = []

    for item in all_items:
        if item.condition == Condition.ONE:
            poor_items.append(item)
        elif item.condition == Condition.TWO:
            fair_items.append(item)
        elif item.condition == Condition.THREE:
            good_items.append(item)
        elif item.condition == Condition.FOUR:
            excellent_items.append(item)

    poor_num = Item.get_total_num(poor_items)
    fair_num = Item.get_total_num(fair_items)
    good_num = Item.get_total_num(good_items)
    excellent_num = Item.get_total_num(excellent_items)

    return render_template('index.html', num_items=num_items, num_buildings=num_buildings, num_rooms=num_rooms, poor=poor_num, fair=fair_num, good=good_num, excellent=excellent_num)


def scanner():
    return render_template('items/scanner.html')


def help():
    return render_template('help/help_home.html')
