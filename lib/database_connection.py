import os
import psycopg
from flask import g
from psycopg.rows import dict_row

class DatabaseConnection:
    DEV_DATABASE_NAME = os.getenv('DEV_DATABASE_NAME', 'chitter_app')
    TEST_DATABASE_NAME = os.getenv('TEST_DATABASE_NAME', 'chitter_app_test')

    def __init__(self, test_mode=False):
        self.test_mode = test_mode
        self.connection = None  # Initialize the connection attribute

    def connect(self):
        try:
            # Use environment variables for sensitive information
            db_name = self._database_name()
            user = os.getenv('DB_USER', 'default_user')
            password = os.getenv('DB_PASSWORD', 'default_password')
            host = os.getenv('DB_HOST', 'localhost')
            port = os.getenv('DB_PORT', '5432')
            sslmode = os.getenv('SSL_MODE', 'require')

            # Build the connection string
            connection_string = (
                f"postgresql://{user}:{password}@{host}:{port}/{db_name}?sslmode={sslmode}"
            )

            # Establish the connection using the psycopg library
            self.connection = psycopg.connect(connection_string, row_factory=dict_row)
        except psycopg.OperationalError as e:
            raise Exception(
                f"Couldn't connect to the database {self._database_name()}! "
                f"Error: {str(e)}"
            )

    def seed(self, sql_filename):
        self._check_connection()
        if not os.path.exists(sql_filename):
            raise Exception(f"File {sql_filename} does not exist")
        with self.connection.cursor() as cursor:
            cursor.execute(open(sql_filename, "r").read())
            self.connection.commit()

    def execute(self, query, params=[]):
        self._check_connection()
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            if cursor.description is not None:
                result = cursor.fetchall()
            else:
                result = None
            self.connection.commit()
            return result

    CONNECTION_MESSAGE = (
        'DatabaseConnection.exec_params: Cannot run a SQL query as '
        'the connection to the database was never opened. Did you '
        'make sure to call first the method DatabaseConnection.connect` '
        'in your app.py file (or in your tests)?'
    )

    def _check_connection(self):
        if self.connection is None:
            raise Exception(self.CONNECTION_MESSAGE)

    def _database_name(self):
        return self.TEST_DATABASE_NAME if self.test_mode else self.DEV_DATABASE_NAME

def get_flask_database_connection(app):
    if not hasattr(g, 'flask_database_connection'):
        g.flask_database_connection = DatabaseConnection(
            test_mode=os.getenv('APP_ENV') == 'test')
        g.flask_database_connection.connect()
    return g.flask_database_connection
