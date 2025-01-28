import patoolib
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from constants import website_link, download_button_ref, folder_dowload_files, folder_data

class DownloadManager:
    def __init__(self, download_dir):
        self.download_dir = download_dir
        self.setup_download_folder()

    def setup_download_folder(self):
        # Ensure the download folder exists
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)

    def configure_browser_options(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # Maximize the browser window
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_dir,  # Set the download directory
            "download.prompt_for_download": False,  # Disable download confirmation prompt
            "download.directory_upgrade": True  # Allow the download folder to be overwritten
        })
        return chrome_options

    def start_browser(self):
        chrome_options = self.configure_browser_options()
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def download_data(self):
        driver = self.start_browser()

        try:
            # Open the desired page
            driver.get(website_link)

            # Wait for the page to load
            time.sleep(3)

            # Find the download button and click it
            download_button = driver.find_element(By.XPATH, download_button_ref)
            download_button.click()

            # Wait for the file download
            self.wait_for_download()

        finally:
            # Close the browser
            driver.quit()

    def wait_for_download(self):
        # Check if any .zip file has been downloaded
        while True:
            files = os.listdir(self.download_dir)
            for file in files:
                if file.endswith('.zip'):
                    print(f".zip file found: {file}")
                    return
            time.sleep(1)


class FileManager:
    def __init__(self, download_dir, data_dir):
        self.download_dir = download_dir
        self.data_dir = data_dir

    def get_file_name(self):
        # Return the name of the first file found in the download directory
        files = os.listdir(self.download_dir)
        return files[0] if files else None

    def extract_rar_file(self):
        file_name = self.get_file_name()
        if file_name:
            print(f"Extracting the file: {file_name}")
            patoolib.extract_archive(os.path.join(self.download_dir, file_name), outdir=self.data_dir)
            os.remove(os.path.join(self.download_dir, file_name))
        else:
            print("No file to extract!")


class FileExtractor:
    def __init__(self):
        self.project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.download_dir = os.path.join(self.project_dir, folder_dowload_files)
        self.data_dir = os.path.join(self.project_dir, folder_data)
        
        self.download_manager = DownloadManager(self.download_dir)
        self.file_manager = FileManager(self.download_dir, self.data_dir)
        
    def run(self):
        print("Starting data download...")
        self.download_manager.download_data()

        print("Starting file extraction...")
        self.file_manager.extract_rar_file()