from barcode import EAN13
from barcode.writer import ImageWriter
import base64
from datetime import date, datetime
from io import BytesIO

from sit_object import SitObject
from room import Room


class Item(SitObject):

    table_name = 'item'

    def __init__(self, db_id: int = None, description: str = None, purchase_price: float = None, purchase_date: date = None, room: Room = None):
        super().__init__(db_id)
        self._description = description
        self._purchase_price = purchase_price
        self._purchase_date = purchase_date
        self._room = room

    def __repr__(self):
        return f'{self.description}'

    def __str__(self):
        return f'{self.description}'

    @property
    def description(self):
        if self._description is None:
            self.populate()

        return self._description

    @property
    def purchase_price(self):
        if self._purchase_price is None:
            self.populate()

        return self._purchase_price

    @property
    def purchase_price_readable(self):
        if self.purchase_price is None:
            return None

        return '${:.2f}'.format(self.purchase_price)

    @property
    def purchase_date(self):
        if self._purchase_date is None:
            self.populate()

        return self._purchase_date

    @property
    def purchase_date_timestamp(self):
        if not self.purchase_date:
            return None

        return datetime.combine(self.purchase_date, datetime.min.time()).timestamp()

    @property
    def room(self):
        if self._room is None:
            self.populate()

        return self._room

    @property
    def barcode(self):
        number = f'{100000000000 + self.id}'

        rv = BytesIO()
        print(number)
        ean = EAN13(str(number), writer=ImageWriter())
        ean.write(rv)

        img_str = base64.b64encode(rv.getvalue())
        return img_str.decode('utf-8')

    def _get_create_params_dict(self):
        return {
            'description': self.description,
            'purchase_price': self._purchase_price,
            'room': self.room.id,
            'purchase_date': self.purchase_date_timestamp if self._purchase_date else None
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        purchase_date_seconds = db_result['purchase_date']
        purchase_date = date.fromtimestamp(purchase_date_seconds) if purchase_date_seconds else None
        purchase_price = float(db_result['purchase_price']) if db_result['purchase_price'] else None
        return Item(db_id=db_result['id'],
                    description=db_result['description'],
                    purchase_price=purchase_price,
                    purchase_date=purchase_date,
                    room=Room(db_id=db_result['room']))
