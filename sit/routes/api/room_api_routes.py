from flask import request, render_template

from building import Building
from item import Item
from room import Room


def create_room():
    bldg_id = int(request.form['roomBldg'])
    room_num = request.form['roomNumber']

    room = Room(building=Building(db_id=bldg_id), number=room_num)
    room.create()

    all_rooms = Room.get_all()

    return render_template('rooms/list_rooms.html', rooms=all_rooms)


def get_room_dropdown():
    item_id = int(request.args['item_id'])
    item_for_rooms = Item.get_by_id(item_id)
    all_rooms = Room.get_all()
    return render_template('rooms/rooms_dropdown.html', rooms=all_rooms, item=item_for_rooms)