from sit_object import SitObject


class Building(SitObject):

    table_name = 'building'

    def __init__(self, db_id: int = None, number: str = None):
        super().__init__(db_id)
        self._number = number

    def __repr__(self):
        return self.number

    def __str__(self):
        return self.number

    def __eq__(self, o):
        if not isinstance(o, Building):
            return False

        return self.number == o.number

    def __hash__(self):
        return hash(self.number)

    @property
    def number(self):
        if self._number is None:
            self.populate()

        return self._number

    def _get_create_params_dict(self):
        return {
            'number': self.number
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Building(db_id=db_result['id'], number=db_result['number'])
