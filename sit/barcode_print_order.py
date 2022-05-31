from datetime import datetime

from sit_object import SitObject
from sit.barcode_print_order_mapping import BarcodePrintOrderMapping


class BarcodePrintOrder(SitObject):

    table_name = 'barcode_print_order'

    def __init__(self, db_id: int = None, initiated: datetime = datetime.now()):
        super().__init__(db_id)
        self._initiated = initiated
        self._items = []

    def __repr__(self):
        return self.initiated

    def __str__(self):
        return self.initiated

    def __eq__(self, o):
        if not isinstance(o, BarcodePrintOrder):
            return False

        return self.initiated == o.initiated

    def __hash__(self):
        return hash(self._initiated)

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

    def _get_create_params_dict(self):
        return {
            'initiated': int(self._initiated.timestamp())
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        initiated_ts = int(db_result['initiated'])
        initiated = datetime.fromtimestamp(initiated_ts)
        return BarcodePrintOrder(db_id=db_result['id'], initiated=initiated)
