import unittest
from ratestask.db import Database
from psycopg2.extensions import connection, cursor
from tests.test_sql import create_table_sql, drop_table_sql


class TestBase(unittest.TestCase):
    db: Database
    conn: connection
    cur: cursor

    def setUp(self) -> None:
        database = Database()
        self.db = database
        self.conn = database.get_connection()
        self.cur = self.conn.cursor()
        self._dropTables()
        self._createTables()

    def tearDown(self) -> None:
        self._dropTables
        self.db.put_connection(self.conn)

    def insertWithDict(self, cur: cursor, table_name, data_dicts) -> None:
        """Uses dicts to insert into a table"""
        columns: list[str] = list(data_dicts[0].keys())
        values: list[str] = [
            tuple(item[column] for column in columns) for item in data_dicts
        ]

        for value in values:
            columns_str: str = ", ".join(columns)
            values_placeholders: str = ", ".join("%s" for _ in columns)

            insert_stmt: str = "INSERT INTO %s (%s) VALUES (%s)" % (
                table_name,
                columns_str,
                values_placeholders,
            )
            cur.execute(insert_stmt, value)
        self.conn.commit()

    def _createTables(self) -> None:
        self.cur.execute(create_table_sql)
        self.conn.commit()

    def _dropTables(self) -> None:
        self.cur.execute(drop_table_sql)
        self.conn.commit()
