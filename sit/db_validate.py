from datetime import datetime
import logging
import sqlite3 as sl
from urllib.request import pathname2url

from barcode_print_order import BarcodePrintOrder
from building import Building
from item import Item
from label import Label
from metainfo import MetaInfo
from room import Room

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

    # META INFO
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS metainfo (
                item_count INT,
                building_count INT,
                room_count INT,
                total_dollar_value TEXT,
                valued_item_count INT,
                poor_item_count INT,
                fair_item_count INT,
                good_item_count INT,
                excellent_item_count INT
            );
        """)

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
                purchase_price INTEGER,
                purchase_price_is_estimate INTEGER DEFAULT 0,
                purchase_date INTEGER,
                end_of_life_date INTEGER,
                room INT REFERENCES room(id) ON DELETE CASCADE,
                photo TEXT,
                condition INTEGER DEFAULT 4,
                quantity INTEGER,
                original_inventory_date INTEGER,
                last_modified_date INTEGER,
                notes TEXT
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

    check_columns()

    with conn:
        conn.execute("""
        UPDATE item SET condition = 4 WHERE condition = 5;
        """)

    # Set Meta Data
    MetaInfo.update_db()


def check_columns():
    check_items()
    check_barcode_print_orders()
    check_labels()


def check_items():
    now = datetime.now()
    column_defs = {
        'photo': 'TEXT',
        'quantity': 'INTEGER',
        'end_of_life_date': 'INTEGER',
        'condition': 'INTEGER DEFAULT 5',
        'original_inventory_date': f'INTEGER DEFAULT {int(now.timestamp())}',
        'last_modified_date': 'INTEGER',
        'purchase_price_is_estimate': 'INTEGER DEFAULT 0',
        'notes': 'TEXT'
    }

    _correct_columns(Item, column_defs)
    _ensure_purchase_price_is_int()


def check_barcode_print_orders():
    column_defs = {
        'order_name': 'TEXT'
    }

    _correct_columns(BarcodePrintOrder, column_defs)


def check_labels():
    column_defs = {
        'text': 'TEXT NOT NULL',
        'label_color_id': 'INT DEFAULT 1',
    }

    _correct_columns(Label, column_defs)
    _check_foreign_key(Label, 'label_color_id', 'id', 'label_color')


def _correct_columns(object_class, column_defs):
    results = object_class.run_query(f"PRAGMA table_info({object_class.table_name});")

    for column in column_defs:
        if not any(result['name'] == column for result in results):
            logging.warning(f'Found missing column in {object_class.table_name}: {column}. Adding now...')
            object_class.run_query(f'ALTER TABLE {object_class.table_name} ADD COLUMN {column} {column_defs[column]}')


def _check_foreign_key(object_class, local_col_name, remote_col_name, remote_table_name):
    results = object_class.run_query(f'PRAGMA foreign_key_list({object_class.table_name});')
    for result in results:
        if result['from'] == local_col_name and result['to'] == remote_col_name and result['table'] == remote_table_name:
            # Found, can assume it is correct & present
            return

    logging.warning(f'Missing foreign key reference - {object_class.table_name}({local_col_name}) -> {remote_table_name}({remote_col_name})')


def _ensure_purchase_price_is_int():
    columns = Item.run_query(f'PRAGMA table_info({Item.table_name});')
    temp_table_name = f'{Item.table_name}_TEMP'

    curr_type = None

    for column in columns:
        if column['name'] == 'purchase_price':
            if column['type'].upper() == 'INTEGER':
                return
            curr_type = column['type']

    logging.error(f'{Item.table_name}\'s \'purchase_price\' is type {curr_type} - should be INTEGER. Attempting to fix...')

    # Get current CREATE TABLE SQL
    table_def_sql = Item.run_query(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{Item.table_name}';")[0]['sql']

    column_defs_str = table_def_sql.split(f"CREATE TABLE {Item.table_name} (")[-1][:-1]
    if column_defs_str[-1] == ')':
        column_defs_str = column_defs_str[:-1]

    column_defs = [col_def.strip() for col_def in column_defs_str.split(',')]
    new_col_defs = []

    for col_def in column_defs:
        if col_def.startswith('purchase_price'):
            new_col_defs.append('purchase_price INTEGER')
        else:
            new_col_defs.append(col_def)

    logging.info(f'Creating temporary duplicate table ({temp_table_name} to house data for conversion...')
    new_create_query = f"CREATE TABLE {temp_table_name} ({', '.join(new_col_defs)});"
    Item.run_query(new_create_query)

    logging.info(f'Copying data from {Item.table_name} -> {temp_table_name}...')
    insert_query = f"INSERT INTO {temp_table_name} SELECT * FROM {Item.table_name};"
    Item.run_query(insert_query)

    logging.info(f'Dropping original table...')
    drop_query = f"DROP TABLE {Item.table_name};"
    Item.run_query(drop_query)

    logging.info(f'Renaming {temp_table_name} -> {Item.table_name}...')
    rename_query = f"ALTER TABLE {temp_table_name} RENAME TO {Item.table_name};"
    Item.run_query(rename_query)
