import logging
import sqlite3 as sl
from urllib.request import pathname2url

from item import Item
from barcode_print_order import BarcodePrintOrder

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
            CREATE TABLE IF NOT EXISTS building (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                number TEXT
            );                
        """)

    # ROOM
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS room (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                number TEXT,
                building INT REFERENCES building(id) ON DELETE CASCADE
            );                
        """)

    # ITEM
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS item (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                purchase_price TEXT,
                purchase_date INTEGER,
                end_of_life_date INTEGER,
                room INT REFERENCES room(id) ON DELETE CASCADE,
                photo TEXT,
                condition INTEGER DEFAULT 4,
                quantity INTEGER
            );
        """)

    # LABEL
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS label (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                label_color_id INT,
                FOREIGN KEY (label_color_id) REFERENCES label_color(id)
            );
        """)

    # LABEL-ITEM MAPPING
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS item_label_map (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                label_id INT NOT NULL,
                item_id INT NOT NULL,
                FOREIGN KEY (label_id) REFERENCES label(id),
                FOREIGN KEY (item_id) REFERENCES item(id)                
            );
        """)

    # LABEL COLORS
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS label_color (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                hex_code TEXT NOT NULL,
                white_text INT NOT NULL
            );
        """)

        # Ensure label colors exist
        from label import LabelColor
        all_colors = LabelColor.get_all()

        if len(all_colors) == 0:
            logging.info('No label colors found - generating defaults...')
            for label_color in LabelColor.generate():
                label_color.create()

    # BARCODE PRINT ORDERS
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS barcode_print_order (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                order_name TEXT NOT NULL,
                initiated INTEGER NOT NULL
            );
        """)

    # BARCODE PRINT ORDER MAPPINGS
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS barcode_print_order_mapping (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                item_id INTEGER NOT NULL
            );
        """)

    with conn:
        conn.execute("""
        UPDATE item SET condition = 4 WHERE condition = 5;
        """)

    check_columns()


def check_columns():
    check_items()
    check_barcode_print_orders()


def check_items():
    column_defs = {
        'photo': 'TEXT',
        'quantity': 'INTEGER',
        'end_of_life_date': 'INTEGER',
        'condition': 'INTEGER DEFAULT 5'
    }

    _correct_columns(Item, column_defs)


def check_barcode_print_orders():
    column_defs = {
        'order_name': 'TEXT'
    }

    _correct_columns(BarcodePrintOrder, column_defs)


def _correct_columns(object_class, column_defs):
    results = object_class.run_query(f"PRAGMA table_info({object_class.table_name});")

    for column in column_defs:
        if not any(result['name'] == column for result in results):
            logging.warning(f'Found missing column in {object_class.table_name}: {column}. Adding now...')
            object_class.run_query(f'ALTER TABLE {object_class.table_name} ADD COLUMN {column} {column_defs[column]}')