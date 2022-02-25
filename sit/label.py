from sit_object import SitObject


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

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Text(db_id=db_result['id'], text=db_result['text'])
