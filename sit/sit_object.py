from abc import ABC, abstractmethod
import sqlite3 as sl


class SitObject(ABC):

    db_name = 'suntree-inventory-tracker.db'
    table_name = None

    def __init__(self, db_id: int = None):
        self.id = db_id

    def create(self):
        create_params = self._get_create_params_dict()

        col_names = [key for key in create_params]
        col_names_for_query = ', '.join(col_names)

        q_marks = ['?' for key in create_params]
        q_marks_for_query = ', '.join(q_marks)

        query = f'INSERT INTO {self.__class__.table_name} ({col_names_for_query}) VALUES ({q_marks_for_query});'
        return self.__class__.run_query(query, tuple(create_params.values()))

    @abstractmethod
    def populate(self):
        pass

    @abstractmethod
    def _get_create_params_dict(self):
        pass

    @staticmethod
    def get_by_id(db_id: int):
        pass

    @staticmethod
    def get_db_conn():
        return sl.connect(SitObject.db_name)

    @classmethod
    def run_query(cls, query: str, params: tuple = None):
        conn = cls.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()

            if params:
                # If given params, pass them to the execute function
                cursor.execute(query, params)
            else:
                # Otherwise, just execute the query without parameters
                cursor.execute(query)

            col_names = [description[0] for description in cursor.description]

            # Get & return the results
            results = cursor.fetchall()

            for result in results:
                result_dict = {}
                for i, col_result in enumerate(result):
                    result_dict[col_names[i]] = col_result

            return result_dict

    @classmethod
    @abstractmethod
    def _get_from_db_result(cls, db_result):
        pass
