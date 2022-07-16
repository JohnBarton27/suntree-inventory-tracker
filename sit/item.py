from barcode.upc import UniversalProductCodeA
from barcode.writer import ImageWriter
import base64
from datetime import date, datetime
from io import BytesIO
from PIL import Image

from condition import Condition
from sit_object import SitObject
from room import Room


class Item(SitObject):

    table_name = 'item'

    def __init__(self,
                 db_id: int = None,
                 description: str = None,
                 purchase_price: float = None,
                 purchase_date: date = None,
                 end_of_life_date: date = None,
                 room: Room = None,
                 photo: str = None,
                 condition: Condition = None,
                 quantity: int = None,
                 original_inventory_date: datetime = None,
                 last_modified_date: datetime = None):
        super().__init__(db_id)
        self._description = description
        self._purchase_price = purchase_price
        self._purchase_date = purchase_date
        self._end_of_life_date = end_of_life_date
        self._room = room
        self._photo = photo
        self._condition = condition
        self._quantity = quantity
        self._original_inventory_date = original_inventory_date
        self._last_modified_date = last_modified_date

    def __repr__(self):
        return f'{self.description}'

    def __str__(self):
        return f'{self.description}'

    def update(self):
        # Update last_modified_date whenever updating
        self._last_modified_date = datetime.now()
        super().update()

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
    def end_of_life_date(self):
        if self._end_of_life_date is None:
            self.populate()

        return self._end_of_life_date

    def update_end_of_life_date(self, end_of_life_date: date):
        if self._end_of_life_date == end_of_life_date:
            return

        self._end_of_life_date = end_of_life_date
        self.update()

    @property
    def end_of_life_date_timestamp(self):
        if not self.end_of_life_date:
            return None

        return datetime.combine(self.end_of_life_date, datetime.min.time()).timestamp()

    @property
    def original_inventory_date(self):
        if self._original_inventory_date is None:
            self.populate()

        return self._original_inventory_date

    @property
    def original_inventory_date_timestamp(self):
        if not self.original_inventory_date:
            return None

        return int(self.original_inventory_date.timestamp())

    @property
    def last_modified_date(self):
        if self._last_modified_date is None:
            self.populate()

        return self._last_modified_date

    @property
    def last_modified_date_timestamp(self):
        if not self.last_modified_date:
            return None

        return int(self.last_modified_date.timestamp())

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

    @property
    def small_photo(self):
        if self.photo is None:
            return None

        img_max_dimension = 100
        image_data = base64.b64decode(self.photo.split(",")[1])
        im_file = BytesIO(image_data)
        img = Image.open(im_file)
        original_format = img.format

        if img.size[0] > img.size[1]:
            # If width > height
            w_percent = (img_max_dimension / float(img.size[0]))
            h_size = int((float(img.size[1]) * float(w_percent)))
            img = img.resize((img_max_dimension, h_size), Image.ANTIALIAS)
        else:
            # If height > width
            h_percent = (img_max_dimension / float(img.size[1]))
            w_size = int((float(img.size[0]) * float(h_percent)))
            img = img.resize((w_size, img_max_dimension), Image.ANTIALIAS)

        buf = BytesIO()
        img.save(buf, format=original_format)
        bytes_im = f'data:image/{original_format.lower()};base64,{base64.b64encode(buf.getvalue()).decode("utf-8")}'
        return bytes_im

    def update_photo(self, photo: str):
        if self._photo == photo:
            return

        self._photo = photo
        self.update()

    @property
    def condition(self):
        if self._condition is None:
            self.populate()

        return self._condition

    def update_condition(self, condition: int):
        if self._condition == condition:
            return

        self._condition = condition
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
    def labels(self):
        from label import Label
        return Label.get_for_item(self)

    def update_labels(self, labels: list):
        from item_label_mapping import ItemLabelMap

        current_labels = self.labels
        for label in labels:
            if label not in current_labels:
                # Create
                ilm = ItemLabelMap(label=label, item=self)
                ilm.create()

        for current_label in current_labels:
            if current_label not in labels:
                # Delete
                print(f'Deleting {current_label}...')
                ilm = ItemLabelMap.get_by_item_and_label(self, current_label)
                ilm.delete()

    @property
    def barcode(self):
        ean_num = self.id + 10000000000
        number = f'{ean_num}'

        rv = BytesIO()
        ean = UniversalProductCodeA(str(number), writer=ImageWriter())
        ean.write(rv)

        img_str = base64.b64encode(rv.getvalue())
        return img_str.decode('utf-8')

    def add_label(self, label):
        from item_label_mapping import ItemLabelMap
        ilm = ItemLabelMap(item=self, label=label)
        ilm.create()

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
            'condition': self.condition.int_value,
            'end_of_life_date': self.end_of_life_date_timestamp if self._end_of_life_date else None,
            'photo': self._photo,
            'quantity': self._quantity,
            'original_inventory_date': self.original_inventory_date_timestamp if self._original_inventory_date else None,
            'last_modified_date': self.last_modified_date_timestamp if self._last_modified_date else None
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        purchase_date_seconds = db_result['purchase_date']
        purchase_date = date.fromtimestamp(purchase_date_seconds) if purchase_date_seconds else None

        end_of_life_date_seconds = db_result['end_of_life_date']
        end_of_life_date = date.fromtimestamp(end_of_life_date_seconds) if end_of_life_date_seconds else None

        original_inventory_date_seconds = db_result['original_inventory_date']
        original_inventory_date = datetime.fromtimestamp(original_inventory_date_seconds) if original_inventory_date_seconds else None

        last_modified_date_seconds = db_result['last_modified_date']
        last_modified_date = datetime.fromtimestamp(last_modified_date_seconds) if last_modified_date_seconds else None

        purchase_price = float(db_result['purchase_price']) if db_result['purchase_price'] else None

        item_id = int(db_result['item_id'] if 'item_id' in db_result else db_result['id'])

        condition = Condition.get_by_value(int(db_result['condition'])) if 'condition' in db_result else None

        return Item(db_id=item_id,
                    description=db_result['description'],
                    purchase_price=purchase_price,
                    purchase_date=purchase_date,
                    end_of_life_date=end_of_life_date,
                    room=Room(db_id=db_result['room']),
                    photo=db_result['photo'],
                    quantity=db_result['quantity'],
                    condition=condition,
                    original_inventory_date=original_inventory_date,
                    last_modified_date=last_modified_date)
