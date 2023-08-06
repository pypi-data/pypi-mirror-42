# noinspection PyProtectedMember
from os import _exit as os_exit
from pandas import read_sql_query, DataFrame
from typing import Union, Iterable, List, Tuple, Dict
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from warnings import warn


class Database(object):
    """Base database class to be extended when connecting to MySQL or PostgreSQL databases"""

    def __init__(self):
        self.conn = None
        self.cur = None
        self.server = None
        self.error_state = False
        self.dialect = None
        self.driver = None
        self.db_user = None
        self.db_password = None
        self.db_host = None
        self.db_name = None

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

    def df_from_query(self, stmt: str, index_col: Union[Iterable[str], str] = None, coerce_float: bool = True,
                      params: Union[List, Tuple, Dict] = None, parse_dates: Union[List, Dict] = None,
                      chunksize: int = None):
        """Returns a pandas dataframe from an SQL query. All parameter defaults match those of read_sql_query.

        :param stmt:  The sql query to be executed by the Cursor object
        :param index_col: Column(s) to set as index(MultiIndex).
        :param coerce_float: Attempts to convert values of non-string, non-numeric objects (like decimal.Decimal) to
            floating point. Useful for SQL result sets.
        :param params: List of parameters to pass to execute method.  The syntax used to pass parameters is database
            driver dependent.
        :param parse_dates:
            - List of column names to parse as dates.
            - Dict of ``{column_name: format string}`` where format string is
              strftime compatible in case of parsing string times, or is one of
              (D, s, ns, ms, us) in case of parsing integer timestamps.
            - Dict of ``{column_name: arg dict}``, where the arg dict corresponds
              to the keyword arguments of :func:`pandas.to_datetime`
              Especially useful with databases without native Datetime support,
              such as SQLite.
        :param chunksize: If specified, return an iterator where `chunksize` is the number of rows to include in
            each chunk.
        :return: DataFrame object
        """

        df: DataFrame = read_sql_query(stmt, self.conn, index_col=index_col, coerce_float=coerce_float, params=params,
                                       parse_dates=parse_dates, chunksize=chunksize)
        return df

    def df_to_table(self, df: DataFrame, name: str, schema: str = None, if_exists: str = 'fail', index: bool = True,
                    index_label: Union[str, List] = None, chunksize: int = None, dtype: dict = None,
                    method: Union[None, str, callable] = None):
        """Write records stored in a DataFrame to a SQL database.

        :param df: DataFrame to convert
        :param name: Name of table to be created
        :param schema: Specify the schema (if database flavor supports this)
        :param if_exists: How to behave if the table already exists
        :param index: Write DataFrame index as a column. Uses index_label as the column name in the table.
        :param index_label: Column label for index column(s). If None is given (default) and index is True, then the
            index names are used. A sequence should be given if the DataFrame uses MultiIndex.
        :param chunksize: Rows will be written in batches of this size at a time. By default, all rows will be written
            at once.
        :param dtype: Specifying the datatype for columns. The keys should be the column names and the values should be
            the SQLAlchemy types or strings for the sqlite3 legacy mode.
        :param method: Controls the SQL insertion clause used:
            None : Uses standard SQL INSERT clause (one per row).
            ‘multi’: Pass multiple values in a single INSERT clause.
            callable with signature (pd_table, conn, keys, data_iter)
        """

        # db_url = f'{self.dialect}+{self.driver}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

        if if_exists not in {None, 'fail', 'replace', 'append'}:
            warn(f"Parameter if_exists has invalid value: {if_exists}. "
                 f"Should be one of {{None, 'fail', 'replace', 'append'}}")
            if_exists = None

        if type(method) == str and not method == 'multi':
            warn(f"Parameter method has invalid value: {method}. Should be one of {{None, 'multi', callable}}")
            method = None

        engine = create_engine(
            URL(
                drivername=f'{self.dialect}+{self.driver}',
                username=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.server.local_bind_port,
                database=self.db_name
            )
        )

        df.to_sql(name=name, con=engine, schema=schema, if_exists=if_exists, index=index, index_label=index_label,
                  chunksize=chunksize, dtype=dtype, method=method)

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
