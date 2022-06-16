from flask import request, render_template

from building import Building
from item import Item
from room import Room


def create_room():
    bldg_id = int(request.form['roomBldg'])
    room_num = request.form['roomNumber']

    bldg = Building(db_id=bldg_id)

    room = Room(building=bldg, number=room_num)
    room.create()

    for_bldg = 'forBuilding' in request.form and request.form['forBuilding'] == 'true'

    if for_bldg:
        # Only get rooms for building
        all_rooms = Room.get_for_building(bldg)
    else:
        all_rooms = Room.get_all()

    return render_template('rooms/list_rooms.html', rooms=all_rooms, show_room_locations=not for_bldg)


def get_room_dropdown():
    item_id = int(request.args['item_id'])
    item_for_rooms = Item.get_by_id(item_id)
    all_rooms = Room.get_all()
    return render_template('rooms/rooms_dropdown.html', rooms=all_rooms, item=item_for_rooms)


def edit_room():
    room_id = int(request.args['id'])

    bldg_id = int(request.form['editRoomBldg'])
    room_num = request.form['editRoomNumber']

    room_to_update = Room.get_by_id(room_id)
    room_to_update.update_building(Building(db_id=bldg_id))
    room_to_update.update_number(room_num)

    return render_template('rooms/room_header.html', room=room_to_update)


def delete_room():
    room_id = int(request.args['id'])
    room_to_delete = Room.get_by_id(room_id)
    room_to_delete.delete()

    return '/rooms'
