from sit_object import SitObject
from building import Building


class Room(SitObject):

    table_name = 'room'
    default_ordering = 'number'

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

    def update_building(self, building: Building):
        if self._building == building:
            return

        self._building = building
        self.update()

    def update_number(self, number: str):
        if self._number == number:
            return

        self._number = number
        self.update()

    def create(self):
        super().create()

        # Update metainfo
        from flask import current_app
        current_app.extensions['meta_info'].room_count += 1
        current_app.extensions['meta_info'].update_in_db()

    def delete(self):
        from item import Item
        for item in Item.get_for_room(self):
            item.delete()

        super().delete()

        # Update metainfo
        from flask import current_app
        current_app.extensions['meta_info'].room_count -= 1
        current_app.extensions['meta_info'].update_in_db()

    @classmethod
    def get_all(cls, order_by: str = None):
        all_rooms = super().get_all(order_by=order_by)

        all_rooms.sort(key=lambda x: x.building.number)

        return all_rooms

    @classmethod
    def get_for_building(cls, building: Building):
        results = cls.run_query(f'SELECT * FROM {cls.table_name} WHERE building=?{cls.get_ordering_str()};', (building.id,))
        return cls._get_multiple_from_db_result(results)

    @classmethod
    def _get_from_db_result(cls, db_result):
        return Room(db_id=db_result['id'], number=db_result['number'], building=Building(db_id=db_result['building']))

    @classmethod
    def get_biggest_rooms(cls, limit: int = 5):
        from item import Item

        all_items = Item.get_all()
        if len(all_items) == 0:
            return []

        room_counts = {}

        for item in all_items:
            room_id = item.room.id
            if room_id in room_counts:
                room_counts[room_id] += item.quantity
            else:
                room_counts[room_id] = item.quantity

        biggest_rooms = []

        if len(room_counts.keys()) < limit:
            limit = len(room_counts.keys())

        for i in range(0, limit):
            room_id = max(room_counts, key=room_counts.get)
            item_count = room_counts[room_id]

            room = Room(db_id=room_id)
            biggest_rooms.append({'room': room, 'count': item_count})

            room_counts.pop(room_id)

        return biggest_rooms
