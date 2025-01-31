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
    
    def delete_all_files(self):
        """
        Deletes all files from the specified directory.

        This function iterates through all files in the directory specified by `data_dir` 
        and removes them one by one.

        Returns:
            None
        """        
        for file in os.listdir(self.data_dir):            
            os.remove(os.path.join(self.data_dir, file))
            print(f"File {file} deleted!")


    def get_files_names(self):
        """
        Retorna uma lista de tuplas com (id, nome) da tabela 'pessoas'.
        
        :return: Lista de tuplas [(id, nome), ...]
        """
        query = f"SELECT id, file_name FROM {table_ingested_files}"
        return self.db.select(query)
    
    def check_files(self):
        """
        Checks which files in the data directory have not been ingested yet.

        The function compares the files present in the `data_dir` directory with the already ingested files  
        (stored in the `ingested_files` DataFrame). It returns a list of files that have not been ingested.  
        Additionally, it ensures that the file with the highest ID is included in the list if it is not already there.

        Returns:
            list: List of file names that have not been ingested.
        """
        self.ingested_files = self.get_files_names()

        file_names = [file for file in os.listdir(self.data_dir) if os.path.isfile(os.path.join(self.data_dir, file))]        

        missing_files = [file for file in file_names if file not in self.ingested_files['file_name'].values]
        
        if not self.ingested_files.empty:
            max_id_row = self.ingested_files.loc[self.ingested_files['id'].idxmax()]
            file_with_max_id = max_id_row['file_name']  
            
            if file_with_max_id not in missing_files:
                missing_files.append(file_with_max_id)
        else:
            file_with_max_id = None

        return missing_files
     

    def process_file_name_return_id(self, file_name):
        """
        Processes the file name and returns its ID.

        If the file has not been ingested yet, it is inserted into the 'ingested_files' table,  
        and the newly generated ID is returned. If the file already exists, the corresponding ID is retrieved.

        Args:
            file_name (str): Name of the file to be processed.

        Returns:
            int: ID of the file in the 'ingested_files' table.
        """
        files = self.get_files_names()                        

        if file_name not in self.ingested_files['file_name'].values:
            self.db.insert(table_ingested_files, ['file_name'], [file_name])
            generated_id = self.db.cursor.lastrowid
            return generated_id
        else:
            id = self.ingested_files.loc[self.ingested_files['file_name'] == file_name, 'id'].iloc[0]
            return id            

    def process_file(self, file_path, file_name):
        """
        Processes a CSV file, adjusts the columns, and inserts the data into the database.
        :param file_path: Path to the CSV file to be processed.
        """
        try:            
            print(f'Starting the file {file_name}')
            file_id = self.process_file_name_return_id(file_name)            
            df = pd.read_csv(file_path, sep=';')
            print('Adjusting the columns.')
            df.columns = df.columns.str.lower()
            df = df.rename(columns={'data': 'ref_data', 'interior/metropolitana': 'interior_metropolitana'})
            df['file_id'] = file_id
            print(f'Deleting duplicated values from the database file_id: {file_id}.')
            self.db.delete(table_name,"file_id = ?",(int(file_id),))
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

        self.delete_all_files()
    
    def run(self):
        self.extract_and_insert()        