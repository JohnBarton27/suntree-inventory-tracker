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
    total_num_items = Item.get_count()

    num_pages = math.ceil(total_num_items / settings.TABLE_PAGE_SIZE)
    return render_template('items/list_items.html', items=items, num_pages=num_pages, selected_page=page_num,
                           page_size=settings.TABLE_PAGE_SIZE, total_items=total_num_items)


def advanced_search_items():
    page_num = int(request.form.get('page', 0))

    where_clauses = []

    description_search = request.form['itemDescSearch']
    if description_search:
        where_clauses.append(f'description LIKE \'%{description_search}%\'')

    lowest_price = request.form.get('itemLowestPrice')
    if lowest_price or lowest_price == 0:  # 0 needs to eval as True
        where_clauses.append(f'purchase_price >= {lowest_price}')

    highest_price = request.form.get('itemHighestPrice')
    if highest_price or highest_price == 0:  # 0 needs to eval as True
        where_clauses.append(f'purchase_price <= {highest_price}')

    earliest_purchase_date_str = request.form.get('itemEarliestPurchaseDate')
    if earliest_purchase_date_str:
        earliest_purchase_date = datetime.strptime(earliest_purchase_date_str, '%Y-%m-%d')
        earliest_purchase_timestamp = int(datetime.timestamp(earliest_purchase_date))
        where_clauses.append(f'purchase_date >= {earliest_purchase_timestamp}')

    latest_purchase_date_str = request.form.get('itemLatestPurchaseDate')
    if latest_purchase_date_str:
        latest_purchase_date = datetime.strptime(latest_purchase_date_str, '%Y-%m-%d')
        latest_purchase_timestamp = int(datetime.timestamp(latest_purchase_date))
        where_clauses.append(f'purchase_date <= {latest_purchase_timestamp}')

    search_building_id = request.form.get('itemBuildingSearch')
    if search_building_id:
        rooms = Room.get_for_building(Building(db_id=int(search_building_id)))
        where_clauses.append(f'({" OR ".join([f"room = {room.id}" for room in rooms])})')

    search_label_id = request.form.get('itemLabelSearch')
    if search_label_id:
        label = Label.get_by_id(int(search_label_id))
        items_in_label = label.get_items()
        where_clauses.append(f'({" OR ".join([f"id = {item.id}" for item in items_in_label])})')

    conditions = []
    if 'poor' in request.form:
        conditions.append(1)
    if 'fair' in request.form:
        conditions.append(2)
    if 'good' in request.form:
        conditions.append(3)
    if 'excellent' in request.form:
        conditions.append(4)

    if conditions:
        where_clauses.append(f'condition in ({",".join([str(condition) for condition in conditions])})')

    where_clause = f' WHERE {" AND ".join(where_clauses)}' if len(where_clauses) >= 1 else ''
    matching_items = Item.get_page(page_num, order_by='description', where_clause=where_clause)
    total_matching_items = Item.get_count(where_clause=where_clause)
    num_pages = math.ceil(total_matching_items / settings.TABLE_PAGE_SIZE)
    return render_template('items/list_items.html', items=matching_items, num_pages=num_pages, selected_page=page_num,
                           page_size=settings.TABLE_PAGE_SIZE, total_items=total_matching_items)


def clear_advanced_search():
    items = Item.get_page(0, order_by='description')
    total_num_items = Item.get_count()

    num_pages = math.ceil(total_num_items / settings.TABLE_PAGE_SIZE)
    return render_template('items/list_items.html', items=items, num_pages=num_pages, selected_page=0,
                           page_size=settings.TABLE_PAGE_SIZE, total_items=total_num_items)


def create_item():
    purchase_date_str = request.form['itemPurchaseDate']
    purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date() if purchase_date_str else None

    end_of_life_date_str = request.form['itemEndOfLifeDate']
    end_of_life_date = datetime.strptime(end_of_life_date_str, '%Y-%m-%d').date() if end_of_life_date_str else None

    purchase_price = float(request.form['itemPurchasePrice']) if request.form['itemPurchasePrice'] else None
    purchase_price_is_estimate = request.form.get("itemPurchasePriceEstimate") is not None

    quantity = int(request.form['itemQuantity']) if request.form['itemQuantity'] else 1
    photo_src = None
    if 'itemPicture' in request.form:
        photo_src = request.form['itemPicture']

    label_ids = request.form.getlist('itemLabels')
    labels = [Label(db_id=int(label_id)) for label_id in label_ids]
    condition = Condition.get_by_value(int(request.form['itemCondition'])) if request.form['itemCondition'] else None

    item = Item(description=request.form['itemDesc'],
                purchase_price=purchase_price,
                purchase_price_is_estimate=purchase_price_is_estimate,
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
    purchase_price_is_estimate = request.form.get("itemPurchasePriceEstimate") is not None

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
    item_to_update.update_purchase_price_is_estimate(purchase_price_is_estimate)
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
