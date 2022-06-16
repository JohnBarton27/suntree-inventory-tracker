from flask import render_template

from building import Building
from room import Room


def buildings():
    all_buildings = Building.get_all()
    return render_template('buildings/buildings.html', buildings=all_buildings)


def building(building_id):
    this_bldg = Building.get_by_id(building_id)
    rooms_in_building = Room.get_for_building(this_bldg)
    return render_template('buildings/building.html', building=this_bldg, rooms=rooms_in_building,
                           show_room_locations=False)
