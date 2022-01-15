from abc import ABC, abstractmethod
import sqlite3 as sl


class SitObject(ABC):

    db_name = 'suntree-inventory-tracker.db'
    table_name = None

    def __init__(self, db_id: int = None):
        self.id = db_id

    def create(self):
        self.__class__._check_for_class_name()

        create_params = self._get_create_params_dict()

        col_names = [key for key in create_params]
        col_names_for_query = ', '.join(col_names)

        q_marks = ['?' for key in create_params]
        q_marks_for_query = ', '.join(q_marks)

        query = f'INSERT INTO {self.__class__.table_name} ({col_names_for_query}) VALUES ({q_marks_for_query});'
        self.id = self.__class__.run_query(query, tuple(create_params.values()))

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

            if query.lower().startswith('insert'):
                # This was an insert - return lastrowid
                return cursor.lastrowid

            if cursor.description is None:
                # If no description is given, there are no 'results'
                return

            col_names = [description[0] for description in cursor.description]

            # Get & return the results
            results = cursor.fetchall()
            structured_results = []

            for result in results:
                result_dict = {}
                for i, col_result in enumerate(result):
                    result_dict[col_names[i]] = col_result

                structured_results.append(result_dict)

            return structured_results

    @classmethod
    @abstractmethod
    def _get_from_db_result(cls, db_result):
        pass

    @classmethod
    def _get_multiple_from_db_result(cls, db_results):
        objs = []

        for db_result in db_results:
            objs.append(cls._get_from_db_result(db_result))

        return objs

    @classmethod
    def get_all(cls):
        cls._check_for_class_name()

        query = f'SELECT * FROM {cls.table_name};'

        results = cls.run_query(query)
        return cls._get_multiple_from_db_result(results)

    @classmethod
    def _check_for_class_name(cls):
        if cls.table_name is None:
            raise Exception(f'The \'table_name\' class variable is undefined for {cls.__name__}!')
