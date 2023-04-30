from enum import Enum
from sit_object import SitObject


from building import Building
from condition import Condition
from item import Item
from room import Room


class MetaInfoCols(Enum):

    ITEM_COUNT = 'item_count'
    BUILDING_COUNT = 'building_count'
    ROOM_COUNT = 'room_count'
    TOTAL_DOLLAR_VALUE = 'total_dollar_value'  # TEXT
    VALUED_ITEM_COUNT = 'valued_item_count'
    POOR_ITEM_COUNT = 'poor_item_count'
    FAIR_ITEM_COUNT = 'fair_item_count'
    GOOD_ITEM_COUNT = 'good_item_count'
    EXCELLENT_ITEM_COUNT = 'excellent_item_count'


class MetaInfo:

    db_name = SitObject.db_name
    table_name = 'metainfo'

    def __init__(self, item_count: int,
                 building_count: int,
                 room_count: int,
                 total_dollar_value: str,
                 valued_item_count: int,
                 poor_item_count: int,
                 fair_item_count: int,
                 good_item_count: int,
                 excellent_item_count: int):
        self.item_count = item_count
        self.building_count = building_count
        self.room_count = room_count
        self.total_dollar_value = total_dollar_value
        self.valued_item_count = valued_item_count
        self.poor_item_count = poor_item_count
        self.fair_item_count = fair_item_count
        self.good_item_count = good_item_count
        self.excellent_item_count = excellent_item_count

    @classmethod
    def get_from_db(cls):
        select_query = f'SELECT * FROM metainfo;'
        result = SitObject.run_query(select_query)[0]

        item_count = result.get(MetaInfoCols.ITEM_COUNT.value)
        building_count = result.get(MetaInfoCols.BUILDING_COUNT.value)
        room_count = result.get(MetaInfoCols.ROOM_COUNT.value)
        total_dollar_value = result.get(MetaInfoCols.TOTAL_DOLLAR_VALUE.value)
        valued_item_count = result.get(MetaInfoCols.VALUED_ITEM_COUNT.value)

        poor_item_count = result.get(MetaInfoCols.POOR_ITEM_COUNT.value)
        fair_item_count = result.get(MetaInfoCols.FAIR_ITEM_COUNT.value)
        good_item_count = result.get(MetaInfoCols.GOOD_ITEM_COUNT.value)
        excellent_item_count = result.get(MetaInfoCols.EXCELLENT_ITEM_COUNT.value)

        return MetaInfo(item_count=item_count,
                        building_count=building_count,
                        room_count=room_count,
                        total_dollar_value=total_dollar_value,
                        valued_item_count=valued_item_count,
                        poor_item_count=poor_item_count,
                        fair_item_count=fair_item_count,
                        good_item_count=good_item_count,
                        excellent_item_count=excellent_item_count)

    def update_in_db(self):
        db_conn = SitObject.get_db_conn()

        table_name = self.__class__.table_name

        with db_conn:
            db_conn.execute(f'DELETE FROM {table_name};')

            insert_query = f"""INSERT into {table_name} ({MetaInfoCols.ITEM_COUNT.value},
                                                         {MetaInfoCols.BUILDING_COUNT.value},
                                                         {MetaInfoCols.ROOM_COUNT.value},
                                                         {MetaInfoCols.TOTAL_DOLLAR_VALUE.value},
                                                         {MetaInfoCols.VALUED_ITEM_COUNT.value},
                                                         {MetaInfoCols.POOR_ITEM_COUNT.value},
                                                         {MetaInfoCols.FAIR_ITEM_COUNT.value},
                                                         {MetaInfoCols.GOOD_ITEM_COUNT.value},
                                                         {MetaInfoCols.EXCELLENT_ITEM_COUNT.value}) 
                        VALUES ({self.item_count},
                                {self.building_count},
                                {self.room_count},
                                {self.total_dollar_value},
                                {self.valued_item_count},
                                {self.poor_item_count},
                                {self.fair_item_count},
                                {self.good_item_count},
                                {self.excellent_item_count});"""

            db_conn.execute(insert_query)

    @classmethod
    def get_from_instance(cls):
        all_items = Item.get_all()

        item_count = len(all_items)
        bldg_count = Building.get_count()
        room_count = Room.get_count()

        total_value_str = '\'${:,.2f}\''.format(Item.get_value(all_items))
        valued_item_count = len([item for item in all_items if item.purchase_price])

        poor_item_count = len([item for item in all_items if item.condition == Condition.ONE])
        fair_item_count = len([item for item in all_items if item.condition == Condition.TWO])
        good_item_count = len([item for item in all_items if item.condition == Condition.THREE])
        excellent_item_count = len([item for item in all_items if item.condition == Condition.FOUR])

        return MetaInfo(item_count, bldg_count, room_count, total_value_str, valued_item_count,
                        poor_item_count, fair_item_count, good_item_count, excellent_item_count)

    @classmethod
    def update_db(cls):
        mi = cls.get_from_instance()
        mi.update_in_db()


