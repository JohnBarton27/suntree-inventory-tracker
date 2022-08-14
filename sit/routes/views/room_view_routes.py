from flask import render_template

from building import Building
from item import Item
from room import Room


def rooms():
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    return render_template('rooms/rooms.html', rooms=all_rooms, buildings=all_buildings, show_room_locations=True)


def room(room_id):
    this_room = Room.get_by_id(room_id)
    items_in_room = Item.get_for_room(this_room)
    all_buildings = Building.get_all()

    total_value_str = '${:,.2f}'.format(Item.get_value(items_in_room))
    percentage_of_valued_items = f"{Item.get_percentage_of_valued(items_in_room):.2%}"

    return render_template('rooms/room.html', room=this_room, items=items_in_room, buildings=all_buildings,
                           show_item_locations=False, room_value=total_value_str,
                           room_percentage_valued=percentage_of_valued_items)
