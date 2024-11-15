import psycopg2
from psycopg2 import sql

from src.db_queries import insert_user_query, check_in_query, check_out_query, is_user_checked_in
    
class Database:
    def __init__(self, dbname, user, password, host='localhost', port=5432):
        """
        Initialize the Database connection.

        :param dbname: Name of the.
        :param user: Username for the.
        :param password: Password for the user.
        :param host: Host where the is located.
        :param port: Port on which the is running.
        """
        self.connection = None
        try:
            self.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )
            print("Database connection successful")
        except Exception as e:
            print(f"Error connecting to: {e}")

    def close(self):
        """Close the connection."""
        if self.connection:
            self.connection.close()
            print("Database connection closed")
        
    def create_table(self, create_table_query):
        """
        Create a table in the.

        :param create_table_query: SQL query for creating the table.
        """
        self.execute_query(create_table_query)


    def execute_query(self, query, data=None, fetch_one=False):
        """
        Execute a single query.

        :param query: SQL query to execute.
        :param data: Data to pass to the query.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            self.connection.commit()
            if fetch_one:
                return cursor.fetchone()

    def fetch_all(self, query, data=None):
        """
        Fetch all results from a query.

        :param query: SQL query to execute.
        :param data: Data to pass to the query.
        :return: List of fetched rows.
        """
        with self.connection.cursor() as cursor:
            cursor.execute(query, data)
            return cursor.fetchall()

    def register_user(self, first_name, last_name='', email='', phone=''):
        """
        Register user and return user_id.
        :return: List of fetched rows.
        """
        return self.execute_query(insert_user_query, (first_name, last_name, email, phone), True)[0]

    def check_in(self, user_id):
        result = self.fetch_all(is_user_checked_in, (user_id,))
        
        if result[0][0] > 0:
            print(f"User {user_id} is already checked in.")
            return
        
        self.execute_query(check_in_query, (user_id,))
        print(f"User {user_id} checked in successfully.")
        return user_id

    def check_out(self, user_id):
        result = self.fetch_all(is_user_checked_in, (user_id,))

        if result[0][0] == 0:
            print(f"User {user_id} is not checked in.")
            return

        self.execute_query(check_out_query, (user_id,))
        print(f"User {user_id} checked out successfully.")
