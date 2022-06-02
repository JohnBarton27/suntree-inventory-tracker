# Standard Packages
import base64
from datetime import datetime
import logging
import numpy as np
import os

# Barcode Reading
import cv2
from pyzbar.pyzbar import decode

# Flask/webapps
from flask import Flask, render_template, request, redirect, url_for
from waitress import serve

# SIT
from building import Building
from condition import Condition
from item import Item
from label import Label, LabelColor
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
    return render_template('buildings/building.html', building=this_bldg, rooms=rooms_in_building, show_room_locations=False)


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
    return render_template('items/items.html', items=all_items, rooms=all_rooms, buildings=all_buildings, labels=all_labels, show_item_locations=True)


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
@app.route('/api/buildings/create', methods=['POST'])
def create_building():
    bldg_num = request.form['bldgNum']

    bldg = Building(number=bldg_num)
    bldg.create()

    all_buildings = Building.get_all()

    return render_template('buildings/list_buildings.html', buildings=all_buildings)


@app.route('/api/rooms/create', methods=['POST'])
def create_room():
    bldg_id = int(request.form['roomBldg'])
    room_num = request.form['roomNumber']

    room = Room(building=Building(db_id=bldg_id), number=room_num)
    room.create()

    all_rooms = Room.get_all()

    return render_template('rooms/list_rooms.html', rooms=all_rooms)


@app.route('/api/labels/create', methods=['POST'])
def create_label():
    label_text = request.form['labelText']

    label_color = LabelColor.get_random()
    label = Label(text=label_text, color=label_color)
    label.create()

    all_labels = Label.get_all()

    return render_template('labels/list_labels.html', labels=all_labels)


@app.route('/api/rooms/get_dropdown', methods=['GET'])
def get_rooms_dropdown():
    item_id = int(request.args['item_id'])
    item_for_rooms = Item.get_by_id(item_id)
    all_rooms = Room.get_all()
    return render_template('rooms/rooms_dropdown.html', rooms=all_rooms, item=item_for_rooms)


@app.route('/api/labels/get_dropdown', methods=['GET'])
def get_labels_dropdown():
    item_id = int(request.args['item_id'])
    item_for_labels = Item.get_by_id(item_id)
    all_labels = Label.get_all()
    labels_on_item = [label.id for label in Label.get_for_item(item_for_labels)]
    return render_template('labels/labels_dropdown.html', labels=all_labels, item=item_for_labels, selected=labels_on_item)


@app.route('/api/items/create', methods=['POST'])
def create_items():
    purchase_date_str = request.form['itemPurchaseDate']
    purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date() if purchase_date_str else None

    end_of_life_date_str = request.form['itemEndOfLifeDate']
    end_of_life_date = datetime.strptime(end_of_life_date_str, '%Y-%m-%d').date() if end_of_life_date_str else None

    purchase_price = float(request.form['itemPurchasePrice']) if request.form['itemPurchasePrice'] else None
    quantity = int(request.form['itemQuantity']) if request.form['itemQuantity'] else 1
    photo_src = None
    if 'itemPicture' in request.form:
        photo_src = request.form['itemPicture']

    label_ids = request.form.getlist('itemLabels')
    labels = [Label(db_id=int(label_id)) for label_id in label_ids]

    item = Item(description=request.form['itemDesc'],
                purchase_price=purchase_price,
                purchase_date=purchase_date,
                end_of_life_date=end_of_life_date,
                room=Room(db_id=int(request.form['itemRoom'])),
                photo=photo_src,
                quantity=quantity)

    item.create()

    for label in labels:
        item.add_label(label)

    all_items = Item.get_all()

    return render_template('items/list_items.html', items=all_items, show_item_locations=True)


@app.route('/api/items/update', methods=['POST'])
def edit_item():
    item_id = int(request.args['id'])

    purchase_date_str = request.form['itemPurchaseDate']
    purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date() if purchase_date_str else None

    end_of_life_date_str = request.form['itemEndOfLifeDate']
    end_of_life_date = datetime.strptime(end_of_life_date_str, '%Y-%m-%d').date() if end_of_life_date_str else None

    purchase_price = float(request.form['itemPurchasePrice']) if request.form['itemPurchasePrice'] else None
    condition = Condition.get_by_value(int(request.form['itemCondition'])) if request.form['itemCondition'] else None
    quantity = int(request.form['itemQuantity']) if request.form['itemQuantity'] else 1
    label_ids = request.form.getlist('itemLabels')
    labels = [Label(db_id=int(label_id)) for label_id in label_ids]

    item_to_update = Item.get_by_id(item_id)
    item_to_update.update_description(request.form['itemDesc'])
    item_to_update.update_purchase_price(purchase_price)
    item_to_update.update_purchase_date(purchase_date)
    item_to_update.update_end_of_life_date(end_of_life_date)
    item_to_update.update_room(Room(db_id=int(request.form['itemRoom'])))
    item_to_update.update_condition(condition)
    item_to_update.update_quantity(quantity)
    item_to_update.update_labels(labels)

    if 'itemPicture' in request.form:
        item_to_update.update_photo(request.form['itemPicture'])

    return render_template('items/item_card.html', item=item_to_update)


@app.route('/api/items/delete', methods=['DELETE'])
def delete_item():
    item_id = int(request.args['id'])
    item_to_delete = Item.get_by_id(item_id)

    item_to_delete.delete()

    return '/items'


@app.route('/api/items/search', methods=['GET'])
def search_items():
    search_term = request.args['search_term']
    all_items = Item.get_all()

    matching_items = [item_to_check for item_to_check in all_items if search_term.lower() in item_to_check.description.lower()]

    return render_template('items/list_items.html', items=matching_items)


@app.route('/api/items/advanced_search', methods=['POST'])
def advanced_search_items():
    all_items = Item.get_all()
    if not request.form:
        return render_template('items/list_items.html', items=all_items)

    description_search = request.form['itemDescSearch']
    lowest_price = int(request.form['itemLowestPrice']) if request.form['itemLowestPrice'] else None
    highest_price = int(request.form['itemHighestPrice']) if request.form['itemHighestPrice'] else None

    earliest_purchase_date = datetime.strptime(request.form['itemEarliestPurchaseDate'], '%Y-%m-%d').date() if request.form['itemEarliestPurchaseDate'] else None
    latest_purchase_date = datetime.strptime(request.form['itemLatestPurchaseDate'], '%Y-%m-%d').date() if request.form['itemLatestPurchaseDate'] else None

    search_building = Building.get_by_id(int(request.form['itemBuildingSearch'])) if request.form['itemBuildingSearch'] else None

    search_label = Label.get_by_id(int(request.form['itemLabelSearch'])) if request.form['itemLabelSearch'] else None

    matching_items = []
    for item_to_check in all_items:
        if description_search and description_search.lower() not in item_to_check.description.lower():
            continue

        if (lowest_price or highest_price) and not item_to_check.purchase_price:
            continue

        if lowest_price and lowest_price > item_to_check.purchase_price:
            continue

        if highest_price and highest_price < item_to_check.purchase_price:
            continue

        if (earliest_purchase_date or latest_purchase_date) and not item_to_check.purchase_date:
            continue

        if earliest_purchase_date and earliest_purchase_date > item_to_check.purchase_date:
            continue

        if latest_purchase_date and latest_purchase_date < item_to_check.purchase_date:
            continue

        if search_building and not item_to_check.room:
            continue

        if search_building and item_to_check.room.building != search_building:
            continue

        if search_label and search_label not in item_to_check.labels:
            continue

        # Match!
        matching_items.append(item_to_check)

    return render_template('items/list_items.html', items=matching_items)


@app.route('/api/scan_barcode', methods=['POST'])
def scan_barcode():
    image_base_64 = request.form['image_source'].split(',')[-1]

    img = base64.b64decode(image_base_64)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    detectedBarcodes = decode(source)

    if len(detectedBarcodes) > 0:
        barcode_val = detectedBarcodes[0].data.decode('utf-8')
        print(detectedBarcodes[0])
        item_id = int(f'{barcode_val}'[:-1]) - 10000000000

        return f'/item/{item_id}'

    return ''


@app.route('/api/printing/create', methods=['POST'])
def create_print_order():
    order_name = request.form['orderNameText']
    initiated = datetime.now()

    barcode_print_order = BarcodePrintOrder(name=order_name, initiated=initiated)
    barcode_print_order.create()

    all_orders = BarcodePrintOrder.get_all()

    return render_template('printing/order_dropdown.html', orders=all_orders)


@app.route('/api/printing/dropdown', methods=['GET'])
def get_printing_order_dropdown():
    all_orders = BarcodePrintOrder.get_all()

    return render_template('printing/order_dropdown.html', print_orders=all_orders)


@app.route('/api/printing/<order_id>/add_item', methods=['POST'])
def add_item_to_print_order(order_id):
    order = BarcodePrintOrder.get_by_id(int(order_id))
    item_id = int(request.form['itemId'])

    item_to_add = Item.get_by_id(item_id)

    order.add_item(item_to_add)

    return 'SUCCESS'



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
