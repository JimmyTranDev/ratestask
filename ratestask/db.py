from os import getenv
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import connection, cursor
from ratestask.sql import GET_RATES_SQL


class Database:
    """Database class with pool of connections"""

    pool: SimpleConnectionPool = None

    def __init__(self):
        self.pool = SimpleConnectionPool(
            5,
            100,
            dbname=getenv("DB_NAME"),
            user=getenv("DB_USER"),
            port=5433 if getenv("RATESTASK_TESTING") else 5432,
            password=getenv("DB_PASSWORD"),
            host="host.docker.internal",

            # Keeps connection alive
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )

    def get_connection(self) -> connection:
        """Gets a database connection from the connection pool"""
        conn = self.pool.getconn()
        return conn

    def put_connection(self, conn: connection) -> None:
        """Puts database connection back into the connection pool"""
        return self.pool.putconn(conn)

    def get_rates(self, date_from, date_to, origin, destination):
        """ Gets daily average rates between two ports/regions"""
        conn: connection = self.get_connection()
        cur: cursor = conn.cursor()
        cur.execute(
            GET_RATES_SQL,
            {
                "date_from": date_from,
                "date_to": date_to,
                "origin": origin,
                "destination": destination,
            },
        )
        rates_result = cur.fetchall()
        cur.close()
        self.put_connection(conn)
        return rates_result
