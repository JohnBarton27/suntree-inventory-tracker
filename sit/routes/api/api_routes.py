import base64
import cv2
import numpy as np
import os
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
        print(detected_barcodes[0])
        item_id = int(f'{barcode_val}'[:-1]) - 10000000000

        return f'/item/{item_id}'

    return ''


def download_database():
    file = pathname2url(settings.DB_NAME)
    print(file)
    return send_file(file, download_name='sit.db')

