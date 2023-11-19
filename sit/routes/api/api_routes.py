import base64
import cv2
import numpy as np
import os
import shutil
from urllib.request import pathname2url
from pyzbar.pyzbar import decode

from flask import request, send_file

import settings


def scan_barcode():
    image_base_64 = request.form['image_source'].split(',')[-1]

    img = base64.b64decode(image_base_64)
    np_img = np.fromstring(img, dtype=np.uint8)
    source = cv2.imdecode(np_img, 1)
    detected_barcodes = decode(source)

    if len(detected_barcodes) > 0:
        barcode_val = detected_barcodes[0].data.decode('utf-8')
        item_id = int(f'{barcode_val}'[:-1]) - 10000000000

        return f'/item/{item_id}'

    return ''


def download_database():
    file = pathname2url(settings.DB_NAME)
    return send_file(file, download_name='sit.db')


def csv_export():
    from csv import DictWriter
    from item import Item

    # Specify the fieldnames (column headers)
    fieldnames = ['id', 'description', 'purchase_price', 'purchase_date', 'room', 'quantity', 'end_of_life_date',
                  'condition', 'original_inventory_date', 'last_modified_date', 'purchase_price_is_estimate', 'notes']

    items = Item.get_all()
    print(f"Found {len(items)} items!")

    # Ensure images_export folder exists
    if not os.path.exists('images_export'):
        os.makedirs('images_export')

    # Open a file in write mode
    with open('images_export/export.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)

        # Write the headers
        writer.writeheader()

        # Write the rows
        for item in items:
            writer.writerow(item.get_csv_export())

            if item.photo:
                imgdata = base64.b64decode(item.photo.split(",")[1])
                filename = f'images_export/{item.id}.png'
                with open(filename, 'wb') as f:
                    f.write(imgdata)

    shutil.make_archive('csv_export', 'zip', 'images_export')

    return send_file('csv_export.zip', download_name='sit_csv_export.zip')