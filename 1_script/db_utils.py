import os
import sqlite3
import pandas as pd

from constants import fodler_database,db_name

class CovidBrasilDB:
    def __init__(self):
        """
        Initializes the class with the database name.
        """
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_name = os.path.join(self.project_dir, fodler_database, db_name)                
        self.connection = None
        self.cursor = None

    def open_connection(self):
        """
        Opens a connection to the database.
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()
            print("Connection opened successfully.")

    def close_connection(self):
        """
        Closes the connection to the database.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            print("Connection closed successfully.")
    
    def select(self, query, params=None):
        """
        Executes a SELECT query on the database and returns the results as a pandas DataFrame.
        
        :param query: The SQL query to execute.
        :param params: Parameters for the query, if any, as a tuple or list.
        :return: A pandas DataFrame containing the query results.
        """
        if not self.connection:
            raise ConnectionError("Database connection is not open.")
        
        if params is None:
            params = []
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
                
        columns = [desc[0] for desc in self.cursor.description]

        df = pd.DataFrame(results, columns=columns)
        
        return df

    def insert(self, table, columns, values):
        """
        Inserts records into the database.
        
        :param table: Name of the table.
        :param columns: Table columns in tuple or list format.
        :param values: Values to be inserted in tuple or list format.
        """
        if not self.connection:
            raise ConnectionError("Database connection is not open.")
        
        columns_str = ", ".join(columns)
        placeholders = ", ".join(["?" for _ in values])
        
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        print("Data inserted successfully.")

    def delete(self, table, condition, condition_values):
        """
        Removes records from the database based on a condition.
        
        :param table: Name of the table.
        :param condition: SQL condition for deletion (e.g., "id = ?").
        :param condition_values: Values for the condition in tuple or list format.
        """
        if not self.connection:
            raise ConnectionError("Database connection is not open.")
        
        query = f"DELETE FROM {table} WHERE {condition}"        
        self.cursor.execute(query, condition_values)
        self.connection.commit()
        print("Data removed successfully.")
    
    def insert_df(self, df, table_name):
        """
        Inserts a Pandas DataFrame into the SQLite database.
        
        :param df: The Pandas DataFrame to be inserted.
        :param table_name: The name of the table in the database.
        """
        if not self.connection:
            raise ConnectionError("Database connection is not open.")
        
        df.to_sql(table_name, self.connection, if_exists='append', index=False)
        print(f"Data inserted into table {table_name} successfully.")
