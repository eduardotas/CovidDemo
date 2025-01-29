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
    
    def get_files_names(self):
        """
        Retorna uma lista de tuplas com (id, nome) da tabela 'pessoas'.
        
        :return: Lista de tuplas [(id, nome), ...]
        """
        query = f"SELECT id, file_name FROM {table_ingested_files}"
        return self.db.select(query)
    
    def check_files(self):        
        ingested_files = (self.get_files_names()) # DF com id,file_name

        file_names = [file for file in os.listdir(self.data_dir) if os.path.isfile(os.path.join(self.data_dir, file))]        

        missing_files = [file for file in file_names if file not in ingested_files['file_name'].values]

        # Encontrar o arquivo com o maior id no DataFrame
        if not ingested_files.empty:
            max_id_row = ingested_files.loc[ingested_files['id'].idxmax()]  # Encontra a linha com o maior id
            file_with_max_id = max_id_row['file_name']  # Nome do arquivo com maior id
            # Adiciona o arquivo com o maior id à lista de arquivos ausentes, se não estiver nela
            if file_with_max_id not in missing_files:
                missing_files.append(file_with_max_id)
        else:
            file_with_max_id = None  # Caso o DataFrame esteja vazio

        return missing_files        

    def process_file_name(self,file_name):
        files = self.get_files_names()
                
        self.db.insert(table_ingested_files,['file_name'],[file_name])        

    def process_file(self, file_path, file_name):
        """
        Processes a CSV file, adjusts the columns, and inserts the data into the database.
        :param file_path: Path to the CSV file to be processed.
        """
        try:            
            print(f'Starting the file {file_name}')
            self.process_file_name(file_name)
            df = pd.read_csv(file_path, sep=';')
            print('Adjusting the columns.')
            df.columns = df.columns.str.lower()
            df = df.rename(columns={'data': 'ref_data', 'interior/metropolitana': 'interior_metropolitana'})
            print('Inserting into the database.')
            self.db.insert_df(df, table_name)
            print(f'Finished processing the file {file_name}!')
        except Exception as e:
            print(f'Error processing the file {file_name}!')
            print(f'Error: {e}')

    def extract_and_insert(self):
        """
        Processes all CSV files in the specified directory and inserts them into the database.
        """
        valid_files = self.check_files()

        if not valid_files:
            print("No files to process")
        else:        
            for file in valid_files:
                file_path = os.path.join(self.data_dir, file)
                file_name = os.path.basename(file_path)
                if os.path.isfile(file_path):
                    self.process_file(file_path, file_name)

    
    def run(self):
        self.extract_and_insert()