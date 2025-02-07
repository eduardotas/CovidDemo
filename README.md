# 📌 Objective

This project is a demonstration of knowledge about code organization, Python, Pandas, and SQLite.

I chose to use SQLite because it is easy for anyone to use this project.

---

# 🚀 How to Use

### 📌 Requirements:

- Python installed.
- Chrome browser.

### 📥 Steps to run the project:

1. Download the repository.
2. Install the required libraries:
   ```sh
   pip install -r requirements.txt
   ```
3. To run the project, execute:
   ```sh
   python run.py
   ```

---

# ⚙️ How It Works

### 🛠️ Process Steps:

1️⃣ **Structure Creation**

- The database and necessary folders will be created automatically.

2️⃣ **Data Download**

- The process will access the [covid.saude.gov.br](https://covid.saude.gov.br/) website and download the ZIP file containing COVID data for Brazil.
- The file will be extracted to the `Data` folder.

3️⃣ **Data Processing**

- The script will read the extracted files and insert the data into the created database.
- If the file has already been ingested previously, it will not be processed again.
- If the file has already been ingested previously **but is the latest available file**, it will be ingested again, and its data will undergo an **update** in the database.

4️⃣ **File Cleanup**

- After ingestion, the used files will be deleted to maintain organization.

---

🔹 **Done! Now you can explore the processed data in the SQLite database!**

