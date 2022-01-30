from barcode import EAN13
from barcode.upc import UniversalProductCodeA
from barcode.writer import ImageWriter
import base64
from datetime import date, datetime
from io import BytesIO

from sit_object import SitObject
from room import Room


class Item(SitObject):

    table_name = 'item'

    def __init__(self, db_id: int = None, description: str = None, purchase_price: float = None, purchase_date: date = None, room: Room = None, photo: str = None, quantity: int = None):
        super().__init__(db_id)
        self._description = description
        self._purchase_price = purchase_price
        self._purchase_date = purchase_date
        self._room = room
        self._photo = photo
        self._quantity = quantity

    def __repr__(self):
        return f'{self.description}'

    def __str__(self):
        return f'{self.description}'

    @property
    def description(self):
        if self._description is None:
            self.populate()

        return self._description

    def update_description(self, description: str):
        if self._description == description:
            return

        self._description = description
        self.update()

    @property
    def purchase_price(self):
        if self._purchase_price is None:
            self.populate()

        return self._purchase_price

    def update_purchase_price(self, purchase_price: float):
        if self._purchase_price == purchase_price:
            return

        self._purchase_price = purchase_price
        self.update()

    @property
    def purchase_price_readable(self):
        if self.purchase_price is None:
            return None

        return '${:.2f}'.format(self.purchase_price)

    def update_purchase_date(self, purchase_date: date):
        if self._purchase_date == purchase_date:
            return

        self._purchase_date = purchase_date
        self.update()

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

    def update_room(self, room: Room):
        if self._room == room:
            return

        self._room = room
        self.update()

    @property
    def photo(self):
        if self._photo is None:
            self.populate()

        return self._photo

    def update_photo(self, photo: str):
        if self._photo == photo:
            return

        self._photo = photo
        self.update()

    @property
    def quantity(self):
        if self._quantity is None:
            self.populate()

        return self._quantity

    def update_quantity(self, quantity: int):
        if self._quantity == quantity:
            return

        self._quantity = quantity
        self.update()

    @property
    def barcode(self):
        ean_num = self.id + 10000000000
        number = f'{ean_num}'

        rv = BytesIO()
        ean = UniversalProductCodeA(str(number), writer=ImageWriter())
        ean.write(rv)

        img_str = base64.b64encode(rv.getvalue())
        return img_str.decode('utf-8')

    @classmethod
    def get_for_room(cls, room: Room):
        results = cls.run_query(f'SELECT * FROM {cls.table_name} WHERE room=?;', (room.id,))
        return cls._get_multiple_from_db_result(results)

    def _get_create_params_dict(self):
        return {
            'description': self.description,
            'purchase_price': self._purchase_price,
            'room': self.room.id,
            'purchase_date': self.purchase_date_timestamp if self._purchase_date else None,
            'photo': self._photo,
            'quantity': self._quantity
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        purchase_date_seconds = db_result['purchase_date']
        purchase_date = date.fromtimestamp(purchase_date_seconds) if purchase_date_seconds else None
        purchase_price = float(db_result['purchase_price']) if db_result['purchase_price'] else None
        return Item(db_id=int(db_result['id']),
                    description=db_result['description'],
                    purchase_price=purchase_price,
                    purchase_date=purchase_date,
                    room=Room(db_id=db_result['room']),
                    photo=db_result['photo'],
                    quantity=db_result['quantity'])
