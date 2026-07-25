import sqlite3
import urllib.request
import json
import re
from datetime import datetime

DB_NAME = "etl_rates.db"
API_URL = "https://open.er-api.com/v6/latest/USD"
CURRENCIES = ["PKR", "EUR", "GBP", "AED", "SAR", "CNY"]

# --- EXTRACT ---
def extract():
    print("Extracting data from API...")
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())
    return data["rates"]

# --- TRANSFORM ---
def transform(rates):
    print("Transforming data...")
    cleaned = []
    for currency in CURRENCIES:
        rate = rates.get(currency)

        # Fix missing
        if rate is None:
            print(f"{currency}: missing — skipping")
            continue

        # Fix string
        if isinstance(rate, str):
            rate = rate.strip()
            rate = re.sub(r'[^0-9.]', '', rate)
            rate = float(rate)

        # Fix negative
        if rate < 0:
            rate = abs(rate)

        # Round to 4 decimal places
        rate = round(rate, 4)
        cleaned.append((currency, rate))

    return cleaned

# --- LOAD ---
def load(cleaned_data):
    print("Loading data into database...")
    conn = sqlite3.connect(DB_NAME)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clean_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            currency TEXT,
            rate REAL,
            loaded_at TEXT
        )
    """)
    loaded_at = datetime.now().isoformat(timespec="seconds")
    for currency, rate in cleaned_data:
        conn.execute(
            "INSERT INTO clean_rates VALUES (NULL, ?, ?, ?)",
            (currency, rate, loaded_at)
        )
    conn.commit()
    conn.close()
    print(f"Loaded {len(cleaned_data)} records successfully.")

# --- RUN ETL ---
rates = extract()
cleaned = transform(rates)
load(cleaned)

