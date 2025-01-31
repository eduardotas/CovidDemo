import sqlite3
import os

class DatabaseCreator:
    def __init__(self, db_name="covid_brasil.db"):
        # Directory where the database will be created
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.project_dir, 'database')
        self.db_directory = os.path.join(os.getcwd(), self.data_dir)
        self.db_name = db_name
        self.db_path = os.path.join(self.db_directory, self.db_name)

        # Creating the database folder if it doesn't exist
        os.makedirs(self.db_directory, exist_ok=True)

    def database_exists(self):
        """Checks if the database already exists."""
        return os.path.exists(self.db_path)

    def create_database_and_tables(self):
        if self.database_exists():
            print(f"The database already exists at: {self.db_path}")
            return

        # Connecting to the database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # SQL script to create the covid_brasil table
        create_covid_brasil_table_query = """
        CREATE TABLE IF NOT EXISTS covid_brasil (
            regiao VARCHAR(50),
            estado VARCHAR(2),
            municipio VARCHAR(100),
            coduf INT,
            codmun INT,
            codRegiaoSaude INT,
            nomeRegiaoSaude VARCHAR(100),
            ref_data DATE,
            semanaEpi INT,
            populacaoTCU2019 INT,
            casosAcumulado INT,
            casosNovos INT,
            obitosAcumulado INT,
            obitosNovos INT,
            Recuperadosnovos INT,
            emAcompanhamentoNovos INT,
            interior_metropolitana INT,
            file_id INT
        );
        """
        
        # SQL script to create the ingested_file table
        create_ingested_file_table_query = """
        CREATE TABLE IF NOT EXISTS ingested_file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name TEXT
        );
        """

        # Executing the SQL commands to create the tables
        cursor.execute(create_covid_brasil_table_query)
        cursor.execute(create_ingested_file_table_query)

        # Committing the changes and closing the connection
        conn.commit()
        conn.close()

        print(f"Database created at: {self.db_path}")
        print("Tables 'covid_brasil' and 'ingested_file' created successfully.")


# Running the code
if __name__ == "__main__":
    db_creator = DatabaseCreator()
    db_creator.create_database_and_tables()