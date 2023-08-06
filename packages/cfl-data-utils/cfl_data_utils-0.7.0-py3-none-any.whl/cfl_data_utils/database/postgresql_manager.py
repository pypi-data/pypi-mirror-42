from psycopg2 import connect as psql_connect
from ._database import Database


class PostgreSQLManager(Database):
    # TODO needs updating to take creds rather than URL -.-
    def __init__(self, url: str):
        """Creates a Cursor object for use throughout the program.

        :param url: The URL of the PostgreSQL instance
        """
        super().__init__()

        self.dialect = 'postgresql'
        self.driver = 'psycopg2'
        self.db_user = None
        self.db_password = None
        self.db_host = None
        self.db_port = None
        self.db_name = None

        try:
            self.conn = psql_connect(url)
        except TypeError:
            exit(f'Invalid URL passed to DB Manager: {url}')
        self.commit()
        self.cur = self.conn.cursor()
