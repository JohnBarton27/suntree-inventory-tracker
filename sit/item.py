from datetime import date

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
    def purchase_date(self):
        if self._purchase_date is None:
            self.populate()

        return self._purchase_date

    @property
    def room(self):
        if self._room is None:
            self.populate()

        return self._room

    def _get_create_params_dict(self):
        return {
            'description': self.description,
            'purchase_price': self._purchase_price,
            'purchase_date': self._purchase_date,
            'room': self.room
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        purchase_date_seconds = db_result['purchase_date']
        purchase_date = date.fromtimestamp(purchase_date_seconds)
        return Item(db_id=db_result['id'], description=db_result['description'], purchase_price=float(db_result['purchase_price']), purchase_date=purchase_date, room=Room(db_id=db_result['room']))