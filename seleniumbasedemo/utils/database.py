#!/usr/bin/env python3

import contextlib
import pymysql
import warnings


class Database(object):
    """ Basic methods for MySQL database operations.

    connect_to_database: connect to MySQL database.
    execute_sql: execute SQL after connecting to MySQL database.

    Attributes:
        config: A dictionary of database settings.
    """

    def __init__(self, **config):
        self.config = config

    @contextlib.contextmanager
    def connect_to_database(self):
        """Connect to MySQL database.

        Connect to MySQL database according to initialized configuration.

        Returns:
            A cursor of connection to MySQL database.

        Raises:
            pymysql.Error: An error occurred connecting to MySQL database.
        """
        conn = pymysql.connect(**self.config)
        cursor = conn.cursor()
        try:
            yield cursor
        except pymysql.Error as error:
            print(f"Error {error.args[0]}: {error.args[1]}")
        finally:
            conn.commit()
            cursor.close()
            conn.close()

    def execute_sql(self, sql):
        """Execute SQL in MySQL database

        Fetch all the rows if executing SELECT SQL.

        Args:
            sql: A single line SQL.

        Returns:
            rows: A tuple consisted of row tuples or empty tuple.
        """
        with self.connect_to_database() as cursor:
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                cursor.execute(sql)
                rows = cursor.fetchall()
            return rows

    def escape(self, string):
        return pymysql.escape_string(string)
