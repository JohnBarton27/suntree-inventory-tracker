from sit_object import SitObject


class BarcodePrintOrderMapping(SitObject):

    table_name = 'barcode_print_order_mapping'

    def __init__(self, db_id: int = None, barcode_print_order = None, item = None):
        super().__init__(db_id)
        self._barcode_print_order = barcode_print_order
        self._item = item

    def __eq__(self, o):
        if not isinstance(o, BarcodePrintOrderMapping):
            return False

        if self.barcode_print_order.id != o.barcode_print_order.id:
            return False

        return self.item.id == o.item.id

    def __hash__(self):
        return hash(f'{self.barcode_print_order.id}{self.item.id}')

    @property
    def barcode_print_order(self):
        if self._barcode_print_order is None:
            self.populate()

        return self._barcode_print_order

    @property
    def item(self):
        if self._item is None:
            self.populate()

        return self._item

    def _get_create_params_dict(self):
        return {
            'order_id': self.barcode_print_order.id,
            'item_id': self.item.id
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        from barcode_print_order import BarcodePrintOrder
        from item import Item

        order = BarcodePrintOrder(db_id=db_result['order_id'])
        item = Item(db_id=db_result['item_id'])

        return BarcodePrintOrderMapping(db_id=db_result['id'], barcode_print_order=order, item=item)

    @classmethod
    def get_for_order(cls, order):
        results = cls.run_query(f'SELECT * FROM {cls.table_name} WHERE order_id=?;', (order.id,))
        return cls._get_multiple_from_db_result(results)
