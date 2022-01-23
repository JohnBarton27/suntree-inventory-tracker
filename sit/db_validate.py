import logging
import sqlite3 as sl
from urllib.request import pathname2url

from item import Item

conn = None


def validate(db_name):
    global conn
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
                    room INT REFERENCES room(id) ON DELETE CASCADE,
                    photo TEXT
                );                
            """)

        return

    check_columns()


def check_columns():
    check_items()


def check_items():
    results = Item.run_query(f"PRAGMA table_info({Item.table_name});")

    column_defs = {
        'photo': 'TEXT'
    }

    for column in column_defs:
        if not any(result['name'] == column for result in results):
            logging.warning(f'Found missing column in {Item.table_name}: {column}. Adding now...')
            Item.run_query(f'ALTER TABLE {Item.table_name} ADD COLUMN {column} {column_defs[column]}')