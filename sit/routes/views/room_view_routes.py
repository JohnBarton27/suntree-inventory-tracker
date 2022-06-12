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
    return render_template('rooms/room.html', room=this_room, items=items_in_room, show_item_locations=False)
