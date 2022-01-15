import logging
import os
import sqlite3 as sl
from urllib.request import pathname2url

from flask import Flask, render_template, request

from building import Building
from room import Room

app = Flask(__name__, template_folder=os.path.abspath('static'))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/buildings')
def buildings():
    all_buildings = Building.get_all()
    return render_template('buildings.html', buildings=all_buildings)


@app.route('/rooms')
def rooms():
    all_rooms = Room.get_all()
    all_buildings = Building.get_all()
    return render_template('rooms.html', rooms=all_rooms, buildings=all_buildings)


# API
@app.route('/api/buildings/create', methods=['POST'])
def create_building():
    bldg_num = request.form['bldgNum']

    bldg = Building(number=bldg_num)
    bldg.create()

    return f'Created Building {bldg.number}'


@app.route('/api/rooms/create', methods=['POST'])
def create_room():
    print(request.form)
    bldg_id = int(request.form['roomBldg'])
    room_num = request.form['roomNumber']

    room = Room(building=Building(db_id=bldg_id), number=room_num)
    room.create()

    return f'Created Room {room}'


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

    app.run(port=9263, debug=False, use_reloader=False)
