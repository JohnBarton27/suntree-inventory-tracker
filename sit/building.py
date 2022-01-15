from sit_object import SitObject


class Building(SitObject):

    table_name = 'building'

    def __init__(self, db_id: int = None, number: str = None):
        super().__init__(db_id)
        self.__number = number

    @property
    def number(self):
        if self.__number is None:
            self.populate()

        return self.__number

    def populate(self):
        pass

    def _get_create_params_dict(self):
        return {
            'number': self.number
        }

    @classmethod
    def _get_from_db_result(cls, db_result):
        pass

