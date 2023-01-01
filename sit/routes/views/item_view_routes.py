from flask import render_template
import math
import time

from building import Building
from item import Item
from label import Label
from room import Room
import settings


def items():
    time.sleep(65)
    all_items = Item.get_all(limit=25, order_by="description")
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    all_labels = Label.get_all()
    total_num_items = Item.get_count()
    num_pages = math.ceil(total_num_items / settings.TABLE_PAGE_SIZE)

    return render_template('items/items.html', items=all_items, rooms=all_rooms, buildings=all_buildings,
                           labels=all_labels, show_item_locations=True, num_pages=num_pages, selected_page=0,
                           page_size=settings.TABLE_PAGE_SIZE, total_items=total_num_items)


def item(item_id):
    this_item = Item.get_by_id(item_id)
    return render_template('items/item.html', item=this_item)
