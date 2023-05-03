from flask import render_template

from metainfo import MetaInfo


def index():
    meta_info = MetaInfo.get_from_db()

    num_buildings = meta_info.building_count
    num_rooms = meta_info.room_count

    num_items = meta_info.item_count

    total_value_str = meta_info.total_dollar_value[1:-1]
    percentage_of_valued_items = f"{meta_info.valued_item_count/num_items:.2%}"

    poor_num = meta_info.poor_item_count
    fair_num = meta_info.fair_item_count
    good_num = meta_info.good_item_count
    excellent_num = meta_info.excellent_item_count

    biggest_rooms = []
    return render_template('index.html', num_items=num_items, num_buildings=num_buildings, num_rooms=num_rooms,
                           poor=poor_num, fair=fair_num, good=good_num, excellent=excellent_num,
                           biggest_rooms=biggest_rooms, total_value=total_value_str,
                           percentage_of_valued_items=percentage_of_valued_items)


def scanner():
    return render_template('items/scanner.html')


def help():
    return render_template('help/help_home.html')
