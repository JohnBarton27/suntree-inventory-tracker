from flask import request, render_template

from building import Building


def create_building():
    bldg_num = request.form['bldgNum']

    bldg = Building(number=bldg_num)
    bldg.create()

    all_buildings = Building.get_all()

    return render_template('buildings/list_buildings.html', buildings=all_buildings)


def delete_building():
    building_id = int(request.args['id'])
    building_to_delete = Building.get_by_id(building_id)

    building_to_delete.delete()

    return '/buildings'
