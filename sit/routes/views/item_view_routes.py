from flask import render_template

from building import Building
from item import Item
from label import Label
from room import Room


def items():
    all_items = Item.get_all()
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    all_labels = Label.get_all()
    return render_template('items/items.html', items=all_items, rooms=all_rooms, buildings=all_buildings,
                           labels=all_labels, show_item_locations=True)


def item(item_id):
    this_item = Item.get_by_id(item_id)
    return render_template('items/item.html', item=this_item)
