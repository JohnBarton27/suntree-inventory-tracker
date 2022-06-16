# Standard Packages
import logging
import os

# Flask/webapps
from flask import Flask
from waitress import serve

app = Flask(__name__, template_folder=os.path.abspath('static'))

# VIEWS
from routes.views import building_view_routes, item_view_routes, label_view_routes, printing_view_routes, room_view_routes, view_routes

# Top Level
app.add_url_rule('/', view_func=view_routes.index)
app.add_url_rule('/scanner', view_func=view_routes.scanner)

# Buildings
app.add_url_rule('/buildings', view_func=building_view_routes.buildings)
app.add_url_rule('/building/<building_id>', view_func=building_view_routes.building)

# Items
app.add_url_rule('/items', view_func=item_view_routes.items)
app.add_url_rule('/item/<item_id>', view_func=item_view_routes.item)

# Labels
app.add_url_rule('/labels', view_func=label_view_routes.get_labels)
app.add_url_rule('/label/<label_id>', view_func=label_view_routes.label)

# Printing
app.add_url_rule('/printing', view_func=printing_view_routes.get_printing_orders)
app.add_url_rule('/printing/<order_id>', view_func=printing_view_routes.print_order)

# Rooms
app.add_url_rule('/rooms', view_func=room_view_routes.rooms)
app.add_url_rule('/room/<room_id>', view_func=room_view_routes.room)


# API
from routes.api import api_routes, building_api_routes, item_api_routes, label_api_routes, printing_api_routes, \
    room_api_routes

# Top Level
app.add_url_rule('/api/scan_barcode', view_func=api_routes.scan_barcode, methods=['POST'])

# Buildings
app.add_url_rule('/api/buildings/create', view_func=building_api_routes.create_building, methods=['POST'])
app.add_url_rule('/api/buildings/delete', view_func=building_api_routes.delete_building, methods=['DELETE'])
app.add_url_rule('/api/buildings/update', view_func=building_api_routes.edit_building, methods=['POST'])

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
app.add_url_rule('/api/rooms/delete', view_func=room_api_routes.delete_room, methods=['DELETE'])
app.add_url_rule('/api/rooms/get_dropdown', view_func=room_api_routes.get_room_dropdown, methods=['GET'])
app.add_url_rule('/api/rooms/update', view_func=room_api_routes.edit_room, methods=['POST'])


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
