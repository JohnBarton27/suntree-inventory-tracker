from datetime import datetime
from flask import request, render_template, send_file

from barcode_print_order import BarcodePrintOrder
from item import Item
from room import Room


def add_item_to_print_order(order_id):
    order = BarcodePrintOrder.get_by_id(int(order_id))
    item_id = int(request.form['itemId'])

    item_to_add = Item.get_by_id(item_id)

    order.add_item(item_to_add)

    return 'SUCCESS'


def export_barcodes(order_id):
    order = BarcodePrintOrder.get_by_id(int(order_id))
    base_url = request.url_root
    order.export_for_printing(base_url)
    return send_file('GFG.pdf', download_name='exported.pdf')


def create_print_order():
    order_name = request.form['orderNameText']
    initiated = datetime.now()

    barcode_print_order = BarcodePrintOrder(name=order_name, initiated=initiated)
    barcode_print_order.create()

    all_orders = BarcodePrintOrder.get_all()

    return render_template('printing/order_dropdown.html', orders=all_orders)


def get_printing_order_dropdown():
    all_orders = BarcodePrintOrder.get_all()

    return render_template('printing/order_dropdown.html', print_orders=all_orders)


def create_order_for_room(room_id):
    this_room = Room.get_by_id(int(room_id))
    room_items = Item.get_for_room(this_room)

    order = BarcodePrintOrder(name=f'{str(this_room)}')
    order.create()

    for room_item in room_items:
        order.add_item(room_item)

    return {'order_id': order.id}
