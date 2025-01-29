from download_covid_file import FileExtractor
from extract_to_db import CovidDataExtractor
from database_creator import DatabaseCreator

def run():
    db_creator = DatabaseCreator()

    if not db_creator.database_exists():
        print("The database does not exist. Creating now...")
        db_creator.create_database_and_tables()

    file_extractor = FileExtractor()
    file_extractor.run()
    
    data_extractor = CovidDataExtractor()
    data_extractor.run()

if __name__ == "__main__":
    run()