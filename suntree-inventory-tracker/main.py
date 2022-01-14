import logging
import os
import sqlite3 as sl
from urllib.request import pathname2url

from flask import Flask, render_template, request

app = Flask(__name__, template_folder=os.path.abspath('static'))

@app.route('/')
def index():
    return render_template('index.html')

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


if __name__ == '__main__':
    # Setup Logging
    logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s', level=logging.INFO)
    logging.info('Starting Suntree Inventory Tracker...')

    # Connect to database
    logging.info('About to connect to database...')
    connect_to_database()
    logging.info('Successfully connected to database.')

    app.run(port=9263, debug=False, use_reloader=False)
