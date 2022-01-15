from sit_object import SitObject
from building import Building


class Room(SitObject):

    table_name = 'room'

    def __init__(self, db_id: int = None, number: str = None, building: Building = None):
        super().__init__(db_id)
        self._number = number
        self._building = building

    def __repr__(self):
        return f'{self.building}-{self.number}'

    def __str__(self):
        return f'{self.building}-{self.number}'

    @property
    def number(self):
        if self._number is None:
            self.populate()

        return self._number

    @property
    def building(self):
        if self._building is None:
            self.populate()

        return self._building

    def _get_create_params_dict(self):
        return {
            'number': self.number,
            'building': self.building.id
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Room(db_id=db_result['id'], number=db_result['number'], building=Building(db_id=db_result['building']))