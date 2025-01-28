import sys
import os
import pandas as pd
from constants import db_name, table_name, table_ingested_files, folder_data, fodler_database
from db_utils import CovidBrasilDB

class CovidDataExtractor:
    def __init__(self):
        """
        Initializes the class with the database path and data directory.
        :param db_path: Path to the SQLite database.
        :param data_dir: Directory containing the CSV files.
        """        
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))        
        self.data_dir = os.path.join(self.project_dir, folder_data)
                
        self.db = CovidBrasilDB()
        self.db.open_connection()
    
    def process_file_name(self,file_path):
        file_name = os.path.basename(file_path)
        self.db.insert(table_ingested_files,['file_name'],[file_name])

    def process_file(self, file_path):
        """
        Processes a CSV file, adjusts the columns, and inserts the data into the database.
        :param file_path: Path to the CSV file to be processed.
        """
        try:
            print(f'Starting the file {file_path}')
            self.process_file_name(file_path)
            df = pd.read_csv(file_path, sep=';')
            print('Adjusting the columns.')
            df.columns = df.columns.str.lower()
            df = df.rename(columns={'data': 'ref_data', 'interior/metropolitana': 'interior_metropolitana'})
            print('Inserting into the database.')
            self.db.insert_df(df, table_name)            
            print(f'Finished processing the file {file_path}!')
        except Exception as e:
            print(f'Error processing the file {file_path}!')
            print(f'Error: {e}')

    def extract_and_insert(self):
        """
        Processes all CSV files in the specified directory and inserts them into the database.
        """
        for file in os.listdir(self.data_dir):
            file_path = os.path.join(self.data_dir, file)
            if os.path.isfile(file_path):
                self.process_file(file_path)
    
    def run(self):
        self.extract_and_insert()