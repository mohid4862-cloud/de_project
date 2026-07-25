import sqlite3
import pandas as pd
from google.cloud import bigquery
import os

# Point to your key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\HP\de_project\key.json"
print("Key file exists:", os.path.exists(r"C:\Users\HP\de_project\key.json"))
# Read from SQLite
conn = sqlite3.connect(r"C:\Users\HP\de_project\etl_rates.db")
df = pd.read_sql("SELECT * FROM clean_rates", conn)
conn.close()

print(f"Loaded {len(df)} rows from SQLite")
print(df.head())

# Upload to BigQuery
client = bigquery.Client(project="currency-pipeline")
table_id = "currency-pipeline.currency_data.clean_rates"

job = client.load_table_from_dataframe(df, table_id)
job.result()

print(f"Uploaded {len(df)} rows to BigQuery successfully!")
