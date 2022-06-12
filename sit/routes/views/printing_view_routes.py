from flask import render_template

from barcode_print_order import BarcodePrintOrder


def get_printing_orders():
    all_orders = BarcodePrintOrder.get_all()
    return render_template('printing/printing.html', print_orders=all_orders)


def print_order(order_id):
    order = BarcodePrintOrder(db_id=int(order_id))
    return render_template('printing/order.html', order=order, items=order.items)
