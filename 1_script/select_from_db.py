from db_utils import CovidBrasilDB

db = CovidBrasilDB()
db.open_connection()

query = """

select count(*) from covid_brasil where file_id = '11'

"""

df = db.select(query)

print(df)

# 140475