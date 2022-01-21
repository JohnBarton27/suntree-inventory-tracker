# Standard Packages
import base64
from datetime import datetime
import logging
import numpy as np
import os
import sqlite3 as sl
from urllib.request import pathname2url

# Barcode Reading
import cv2
from pyzbar.pyzbar import decode

# Flask/webapps
from flask import Flask, render_template, request
from waitress import serve

# SIT
from building import Building
from item import Item
from room import Room

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buildings')
def buildings():
    all_buildings = Building.get_all()
    return render_template('buildings/buildings.html', buildings=all_buildings)


@app.route('/rooms')
def rooms():
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    return render_template('rooms/rooms.html', rooms=all_rooms, buildings=all_buildings)


@app.route('/items')
def items():
    all_items = Item.get_all()
    all_rooms = Room.get_all()
    return render_template('items/items.html', items=all_items, rooms=all_rooms)


@app.route('/item/<item_id>')
def item(item_id):
    this_item = Item.get_by_id(item_id)
    return render_template('items/item.html', item=this_item)


@app.route('/scanner')
def scanner():
    return render_template('items/scanner.html')


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


@app.route('/api/items/create', methods=['POST'])
def create_items():
    purchase_date_str = request.form['itemPurchaseDate']
    purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date() if purchase_date_str else None
    purchase_price = float(request.form['itemPurchasePrice']) if request.form['itemPurchasePrice'] else None
    item = Item(description=request.form['itemDesc'],
                purchase_price=purchase_price,
                purchase_date=purchase_date,
                room=Room(db_id=int(request.form['itemRoom'])))

    item.create()

    all_items = Item.get_all()

    return render_template('items/list_items.html', items=all_items)


@app.route('/api/scan_barcode', methods=['POST'])
def scan_barcode():
    image_base_64 = request.form['image_source'].split(',')[-1]

    img = base64.b64decode(image_base_64)
    npimg = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(npimg, 1)
    detectedBarcodes = decode(source)

    if len(detectedBarcodes) > 0:
        return detectedBarcodes[0].data.decode('utf-8')

    return ''


def connect_to_database():
    db_name = 'suntree-inventory-tracker.db'
    try:
        dburi = 'file:{}?mode=rw'.format(pathname2url(db_name))
        conn = sl.connect(dburi, uri=True)
        logging.info('Found existing database.')
    except sl.OperationalError:
        # handle missing database case
        logging.warning('Could not find database - will initialize an empty one!')
        conn = sl.connect(db_name)

        # BUILDING
        with conn:
            conn.execute("""
                CREATE TABLE building (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    number TEXT
                );                
            """)

        # ROOM
        with conn:
            conn.execute("""
                CREATE TABLE room (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    number TEXT,
                    building INT REFERENCES building(id) ON DELETE CASCADE
                );                
            """)

        # ITEM
        with conn:
            conn.execute("""
                CREATE TABLE item (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    description TEXT NOT NULL,
                    purchase_price TEXT,
                    purchase_date INTEGER,
                    room INT REFERENCES room(id) ON DELETE CASCADE
                );                
            """)


if __name__ == '__main__':
    # Setup Logging
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
    logging.info('Starting Suntree Inventory Tracker...')

    # Connect to database
    logging.info('About to connect to database...')
    connect_to_database()
    logging.info('Successfully connected to database.')

    serve(app, host='0.0.0.0', port=9263)
