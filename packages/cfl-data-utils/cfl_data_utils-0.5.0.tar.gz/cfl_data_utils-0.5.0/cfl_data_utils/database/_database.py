# noinspection PyProtectedMember
from os import _exit as os_exit
from pandas import read_sql_query


class Database(object):
    """Base database class to be extended when connecting to MySQL or PostgreSQL databases"""

    def __init__(self):
        self.conn = None
        self.cur = None
        self.error_state = False

    def query(self, sql: str, commit: bool = True):
        """Executes a query passed in by using the DatabaseManager object

        :param sql: The sql query to be executed by the Cursor object
        :param commit: Committing on queries can be disabled for rapid writing (e.g. q_one commit at end)
        :return: the Cursor object
        """

        self.cur.execute(sql)
        if commit:
            self.commit()
        return self.cur

    def df_from_query(self, stmt: str):
        """returns a pandas dataframe from an SQL query

        :param stmt:  The sql query to be executed by the Cursor object
        :return: dataframe object
        """

        df = read_sql_query(stmt, self.conn)
        return df

    def executemany(self, stmt: str, data):
        """Executes a query passed in by using the DatabaseManager object

        :param stmt: The query to be executed by the Cursor object
        :param data: The data to be processed
        :return: the Cursor object
        """

        self.cur.executemany(stmt, data)
        return self.cur

    def commit(self):
        """Commits all changes to database

        :return: the Cursor object
        """

        self.conn.commit()
        return self.cur

    def close(self, force_exit: bool = False):
        """Terminates the database connection

        :param force_exit: Tells the db to completely quit the program
        """
        self.__del__()
        if force_exit:
            os_exit(0)

    def __del__(self):
        """Overrides the close method for the cursor, and ensure proper disconnection from the database"""
        try:
            try:
                self.commit()
            except Exception as err:
                if not self.error_state:
                    print(f'Unable to commit before closing: {err}')
            self.conn.close()
            if not self.error_state:
                print('Connection closed.')
        except AttributeError:
            if not self.error_state:
                print('Unable to close connection.')
