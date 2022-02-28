from sit_object import SitObject
from item import Item
from label import Label


class ItemLabelMap(SitObject):

    table_name = 'item_label_map'

    def __init__(self, db_id: int = None, item: Item = None, label: Label = None):
        super().__init__(db_id)
        self._item = item
        self._label = label

    def __repr__(self):
        return f'{repr(self.item)} - {repr(self.label)}'

    def __str__(self):
        return f'{str(self.item)} - {str(self.label)}'

    def __eq__(self, o):
        if not isinstance(o, ItemLabelMap):
            return False

        if self.item != o.item:
            return False

        return self.label == o.label

    def __hash__(self):
        return hash(f'{hash(self.item)}{hash(self.label)}')

    @property
    def item(self):
        if self._item is None:
            self.populate()

        return self._item

    @property
    def label(self):
        if self._label is None:
            self.populate()

        return self._label

    def _get_create_params_dict(self):
        return {
            'item_id': self.item.id,
            'label_id': self.label.id
        }

    @classmethod
    def get_by_item_and_label(cls, item: Item, label: Label):
        results = cls.run_query(f'SELECT * FROM {cls.table_name} WHERE item_id=? AND label_id=?;', (item.id, label.id))
        return cls._get_from_db_result(results[0])

    @classmethod
    def get_by_item(cls, item: Item):
        results = cls.run_query(f'SELECT * FROM {cls.table_name} WHERE item_id=?;', (item.id,))
        return cls._get_multiple_from_db_result(results)

    @classmethod
    def _get_from_db_result(cls, db_result):
        item = Item(db_result['item_id'])
        label = Label(db_result['label_id'])
        return ItemLabelMap(db_id=db_result['id'], item=item, label=label)
