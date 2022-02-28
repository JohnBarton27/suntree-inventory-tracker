from sit_object import SitObject
from item import Item


class Label(SitObject):

    table_name = 'label'

    def __init__(self, db_id: int = None, text: str = None):
        super().__init__(db_id)
        self._text = text

    def __repr__(self):
        return self.text

    def __str__(self):
        return self.text

    def __eq__(self, o):
        if not isinstance(o, Label):
            return False

        return self.text == o.text

    def __hash__(self):
        return hash(self.text)

    @property
    def text(self):
        if self._text is None:
            self.populate()

        return self._text

    def _get_create_params_dict(self):
        return {
            'text': self.text
        }

    def get_items(self):
        from item_label_mapping import ItemLabelMap
        results = self.__class__.run_query(f'SELECT * FROM {ItemLabelMap.table_name} INNER JOIN item ON item.id == item_label_map.item_id WHERE label_id=?;', (self.id,))
        return Item._get_multiple_from_db_result(results)

    @classmethod
    def get_for_item(cls, item: Item):
        from item_label_mapping import ItemLabelMap
        results = cls.run_query(f'SELECT label_id as id, text FROM {ItemLabelMap.table_name} INNER JOIN {Label.table_name} ON {Label.table_name}.id == {ItemLabelMap.table_name}.label_id WHERE item_id=?;', (item.id,))
        return cls._get_multiple_from_db_result(results)

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Label(db_id=db_result['id'], text=db_result['text'])
