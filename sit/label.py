import random

from sit_object import SitObject
from item import Item


class LabelColor(SitObject):

    table_name = 'label_color'

    def __init__(self, db_id: int = None, hex_code: str = None, white_text: bool = True):
        super().__init__(db_id)
        self._hex_code = hex_code
        self._white_text = white_text

    @property
    def hex_code(self):
        if self._hex_code is None:
            self.populate()

        return self._hex_code

    @property
    def white_text(self):
        if self._white_text is None:
            self.populate()

        return self._white_text

    @staticmethod
    def generate():
        blue_jeans = LabelColor(hex_code='#5DA9E9')
        bone = LabelColor(hex_code='#DDDBCB', white_text=False)
        dark_cornflower_blue = LabelColor(hex_code='#003F91')
        charcoal = LabelColor(hex_code='#3C474B')
        light_coral = LabelColor(hex_code='#FF7073')
        middle_blue_green = LabelColor(hex_code='#9EEFE5', white_text=False)
        midnight = LabelColor(hex_code='#6D326D')
        steel_blue = LabelColor(hex_code='#4F7CAC')
        return [blue_jeans, bone, charcoal, dark_cornflower_blue, light_coral, middle_blue_green, midnight, steel_blue]

    @staticmethod
    def get_random():
        all_colors = LabelColor.get_all()
        return random.choice(all_colors)

    def _get_create_params_dict(self):
        return {
            'hex_code': self.hex_code,
            'white_text': self.white_text
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        use_white_text = db_result['white_text'] == 1
        return LabelColor(db_id=db_result['id'], hex_code=db_result['hex_code'], white_text=use_white_text)


class Label(SitObject):

    table_name = 'label'

    def __init__(self, db_id: int = None, text: str = None, color: LabelColor = None):
        super().__init__(db_id)
        self._text = text
        self._color = color

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

    @property
    def color(self):
        if self._color is None:
            self.populate()

        return self._color

    def update_text(self, text: str):
        if self._text == text:
            return

        self._text = text
        self.update()

    def _get_create_params_dict(self):
        return {
            'text': self.text,
            'label_color_id': self.color.id
        }

    def get_items(self):
        from item_label_mapping import ItemLabelMap
        results = self.__class__.run_query(f'SELECT * FROM {ItemLabelMap.table_name} INNER JOIN item ON item.id == item_label_map.item_id WHERE label_id=?;', (self.id,))
        return Item._get_multiple_from_db_result(results)

    @classmethod
    def get_for_item(cls, item: Item):
        from item_label_mapping import ItemLabelMap
        results = cls.run_query(f'SELECT label_id as id, text, label_color_id FROM {ItemLabelMap.table_name} INNER JOIN {Label.table_name} ON {Label.table_name}.id == {ItemLabelMap.table_name}.label_id WHERE item_id=?;', (item.id,))
        return cls._get_multiple_from_db_result(results)

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Label(db_id=db_result['id'], text=db_result['text'], color=LabelColor(db_id=int(db_result['label_color_id'])))
