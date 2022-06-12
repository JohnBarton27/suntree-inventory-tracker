# Standard Packages
import logging
import os

# Flask/webapps
from flask import Flask, render_template
from waitress import serve

# SIT
from building import Building
from item import Item
from label import Label
from room import Room
from barcode_print_order import BarcodePrintOrder

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def index():
    num_items = len(Item.get_all())
    num_buildings = len(Building.get_all())
    num_rooms = len(Room.get_all())
    return render_template('index.html', num_items=num_items, num_buildings=num_buildings, num_rooms=num_rooms)


@app.route('/buildings')
def buildings():
    all_buildings = Building.get_all()
    return render_template('buildings/buildings.html', buildings=all_buildings)


@app.route('/building/<building_id>')
def building(building_id):
    this_bldg = Building.get_by_id(building_id)
    rooms_in_building = Room.get_for_building(this_bldg)
    return render_template('buildings/building.html', building=this_bldg, rooms=rooms_in_building,
                           show_room_locations=False)


@app.route('/rooms')
def rooms():
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    return render_template('rooms/rooms.html', rooms=all_rooms, buildings=all_buildings, show_room_locations=True)


@app.route('/room/<room_id>')
def room(room_id):
    this_room = Room.get_by_id(room_id)
    items_in_room = Item.get_for_room(this_room)
    return render_template('rooms/room.html', room=this_room, items=items_in_room, show_item_locations=False)


@app.route('/items')
def items():
    all_items = Item.get_all()
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    all_labels = Label.get_all()
    return render_template('items/items.html', items=all_items, rooms=all_rooms, buildings=all_buildings,
                           labels=all_labels, show_item_locations=True)


@app.route('/item/<item_id>')
def item(item_id):
    this_item = Item.get_by_id(item_id)
    return render_template('items/item.html', item=this_item)


@app.route('/scanner')
def scanner():
    return render_template('items/scanner.html')


@app.route('/labels')
def get_labels():
    all_labels = Label.get_all()
    return render_template('labels/labels.html', labels=all_labels)


@app.route('/label/<label_id>')
def label(label_id):
    label = Label(db_id=int(label_id))
    items = label.get_items()
    return render_template('labels/label.html', label=label, items=items)


@app.route('/printing')
def get_printing_orders():
    all_orders = BarcodePrintOrder.get_all()
    return render_template('printing/printing.html', print_orders=all_orders)


@app.route('/printing/<order_id>')
def print_order(order_id):
    order = BarcodePrintOrder(db_id=int(order_id))
    return render_template('printing/order.html', order=order, items=order.items)


# API
from routes.api import api_routes, building_api_routes, item_api_routes, label_api_routes, printing_api_routes, \
    room_api_routes

# Top Level
app.add_url_rule('/api/scan_barcode', view_func=api_routes.scan_barcode, methods=['POST'])

# Buildings
app.add_url_rule('/api/buildings/create', view_func=building_api_routes.create_building, methods=['POST'])

# Items
app.add_url_rule('/api/items/<item_id>', view_func=item_api_routes.get_barcode_for_item, methods=['GET'])
app.add_url_rule('/api/items/advanced_search', view_func=item_api_routes.advanced_search_items, methods=['POST'])
app.add_url_rule('/api/items/create', view_func=item_api_routes.create_item, methods=['POST'])
app.add_url_rule('/api/items/delete', view_func=item_api_routes.delete_item, methods=['DELETE'])
app.add_url_rule('/api/items/search', view_func=item_api_routes.search_items, methods=['GET'])
app.add_url_rule('/api/items/update', view_func=item_api_routes.edit_item, methods=['POST'])

# Labels
app.add_url_rule('/api/labels/create', view_func=label_api_routes.create_label, methods=['POST'])
app.add_url_rule('/api/labels/get_dropdown', view_func=label_api_routes.get_label_dropdown, methods=['GET'])

# Printing
app.add_url_rule('/api/printing/<order_id>/add_item', view_func=printing_api_routes.add_item_to_print_order, methods=['POST'])
app.add_url_rule('/api/printing/<order_id>/export', view_func=printing_api_routes.export_barcodes, methods=['GET'])
app.add_url_rule('/api/printing/create', view_func=printing_api_routes.create_print_order, methods=['POST'])
app.add_url_rule('/api/printing/dropdown', view_func=printing_api_routes.get_printing_order_dropdown, methods=['GET'])
app.add_url_rule('/api/printing/forRoom/<room_id>', view_func=printing_api_routes.create_order_for_room, methods=['POST'])

# Rooms
app.add_url_rule('/api/rooms/create', view_func=room_api_routes.create_room, methods=['POST'])
app.add_url_rule('/api/rooms/get_dropdown', view_func=room_api_routes.get_room_dropdown, methods=['GET'])


def connect_to_database():
    from db_validate import validate
    db_name = 'suntree-inventory-tracker.db'
    validate(db_name)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Suntree Inventory Tracker')

    args = parser.parse_args()

    # Setup Logging
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
    logging.info('Starting Suntree Inventory Tracker...')

    # Connect to database
    logging.info('About to connect to database...')
    connect_to_database()
    logging.info('Successfully connected to database.')

    serve(app, host='0.0.0.0', port=9263)
