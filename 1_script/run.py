from download_covid_file import FileExtractor
from extract_to_db import CovidDataExtractor

def run():
    file_extractor = FileExtractor()
    file_extractor.run()
    data_extractor = CovidDataExtractor()
    data_extractor.run()

if __name__ == "__main__":
    run()