from datetime import datetime
from flask import request, render_template, send_file
import math

from building import Building
from condition import Condition
from item import Item
from label import Label
from room import Room
import settings


def get_barcode_for_item(item_id):
    item_for_barcode = Item.get_by_id(int(item_id))
    import base64
    import io

    f = base64.b64decode(item_for_barcode.barcode)
    f = io.BytesIO(f)

    return send_file(f, download_name='barcode.png')


def get_items_page():
    data = request.form
    page_num = int(data['page'])

    items = Item.get_page(page_num, order_by='description')

    num_pages = math.ceil(Item.get_count() / settings.TABLE_PAGE_SIZE)
    return render_template('items/list_items.html', items=items, num_pages=num_pages, selected_page=page_num)


def advanced_search_items():
    all_items = Item.get_all()
    if not request.form:
        return render_template('items/list_items.html', items=all_items)

    description_search = request.form['itemDescSearch']
    lowest_price = int(request.form['itemLowestPrice']) if request.form['itemLowestPrice'] else None
    highest_price = int(request.form['itemHighestPrice']) if request.form['itemHighestPrice'] else None

    earliest_purchase_date = datetime.strptime(request.form['itemEarliestPurchaseDate'], '%Y-%m-%d').date() if \
        request.form['itemEarliestPurchaseDate'] else None
    latest_purchase_date = datetime.strptime(request.form['itemLatestPurchaseDate'], '%Y-%m-%d').date() if request.form[
        'itemLatestPurchaseDate'] else None

    search_building = Building.get_by_id(int(request.form['itemBuildingSearch'])) if request.form[
        'itemBuildingSearch'] else None

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


def create_item():
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
    condition = Condition.get_by_value(int(request.form['itemCondition'])) if request.form['itemCondition'] else None

    item = Item(description=request.form['itemDesc'],
                purchase_price=purchase_price,
                purchase_date=purchase_date,
                end_of_life_date=end_of_life_date,
                room=Room(db_id=int(request.form['itemRoom'])),
                photo=photo_src,
                quantity=quantity,
                condition=condition,
                original_inventory_date=datetime.now())

    item.create()

    for label in labels:
        item.add_label(label)

    return {'id': item.id}


def delete_item():
    item_id = int(request.args['id'])
    item_to_delete = Item.get_by_id(item_id)

    item_to_delete.delete()

    return '/items'


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


def search_items():
    search_term = request.args['search_term']
    all_items = Item.get_all()

    matching_items = [item_to_check for item_to_check in all_items if
                      search_term.lower() in item_to_check.description.lower()]

    return render_template('items/list_items.html', items=matching_items)
