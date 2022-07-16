from flask import render_template
import math

from building import Building
from item import Item
from label import Label
from room import Room
import settings


def items():
    all_items = Item.get_all(limit=25, order_by="description")
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    all_labels = Label.get_all()

    num_pages = math.ceil(Item.get_count() / settings.TABLE_PAGE_SIZE)

    return render_template('items/items.html', items=all_items, rooms=all_rooms, buildings=all_buildings,
                           labels=all_labels, show_item_locations=True, num_pages=num_pages, selected_page=0)


def item(item_id):
    this_item = Item.get_by_id(item_id)
    return render_template('items/item.html', item=this_item)
