from datetime import datetime

from sit_object import SitObject
from sit.barcode_print_order_mapping import BarcodePrintOrderMapping


class BarcodePrintOrder(SitObject):

    table_name = 'barcode_print_order'

    def __init__(self, db_id: int = None, name: str = None, initiated: datetime = datetime.now()):
        super().__init__(db_id)
        self._name = name
        self._initiated = initiated
        self._items = []

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    def __eq__(self, o):
        if not isinstance(o, BarcodePrintOrder):
            return False

        return self.initiated == o.initiated

    def __hash__(self):
        return hash(self._initiated)

    @property
    def name(self):
        if self._name is None:
            self.populate()

        return self._name

    @property
    def initiated(self):
        if self._initiated is None:
            self.populate()

        return self._initiated

    @property
    def items(self):
        if len(self._items) == 0:
            mappings = BarcodePrintOrderMapping.get_for_order(self)

            for mapping in mappings:
                self._items.append(mapping.item)

        return self._items

    def add_item(self, item):
        new_mapping = BarcodePrintOrderMapping(barcode_print_order=self, item=item)
        new_mapping.create()

        self._items.append(item)

    def remove_item(self, item):
        mapping_to_remove = BarcodePrintOrderMapping(barcode_print_order=self, item=item)
        mapping_to_remove.delete()

        self._items.remove(item)

    def _get_create_params_dict(self):
        return {
            'order_name': self._name,
            'initiated': int(self._initiated.timestamp())
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        initiated_ts = int(db_result['initiated'])
        initiated = datetime.fromtimestamp(initiated_ts)
        return BarcodePrintOrder(db_id=db_result['id'], name=db_result['order_name'], initiated=initiated)
