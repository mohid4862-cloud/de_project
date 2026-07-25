"""
Your first mini data pipeline.
Pulls live currency exchange rates -> stores in SQLite -> runs SQL queries.

No API key needed. No installs needed (sqlite3 and requests-free version below).

HOW TO RUN:
    python first_pipeline.py

Run it a few times over a few days (or a few minutes apart) — each run
adds a new snapshot row, so your SQL queries start returning something
interesting instead of just one row.
"""

import sqlite3
import urllib.request
import json
from datetime import datetime

DB_NAME = "rates.db"
API_URL = "https://open.er-api.com/v6/latest/USD"  # free, no key required


def fetch_rates():
    """Step 1: PULL data from an API."""
    print("Fetching latest exchange rates...")
    with urllib.request.urlopen(API_URL) as response:
        data = json.loads(response.read().decode())
    return data


def setup_database(conn):
    """Create the table if it doesn't exist yet."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS exchange_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            base_currency TEXT,
            target_currency TEXT,
            rate REAL,
            pulled_at TEXT
        )
    """)
    conn.commit()


def store_rates(conn, data):
    """Step 2: STORE the pulled data into SQLite."""
    base = data["base_code"]
    rates = data["rates"]
    pulled_at = datetime.now().isoformat(timespec="seconds")

    # We'll just track a handful of currencies relevant to you (PKR + majors)
    currencies_to_track = ["PKR", "EUR", "GBP", "AED", "SAR", "CNY"]

    rows = [
        (base, cur, rates[cur], pulled_at)
        for cur in currencies_to_track
        if cur in rates
    ]

    conn.executemany("""
        INSERT INTO exchange_rates (base_currency, target_currency, rate, pulled_at)
        VALUES (?, ?, ?, ?)
    """, rows)
    conn.commit()
    print(f"Stored {len(rows)} rate(s) at {pulled_at}")


def run_sample_queries(conn):
    """Step 3: QUERY the data you've stored, using SQL you already know."""
    print("\n--- Query 1: Latest rate for each currency ---")
    for row in conn.execute("""
        SELECT target_currency, rate, MAX(pulled_at) as latest
        FROM exchange_rates
        GROUP BY target_currency
        ORDER BY target_currency
    """):
        print(row)

    print("\n--- Query 2: How many snapshots have we collected? ---")
    for row in conn.execute("SELECT COUNT(*) as total_snapshots FROM exchange_rates"):
        print(row)

    print("\n--- Query 3: PKR rate history (run this script a few times to see it grow) ---")
    for row in conn.execute("""
        SELECT rate, pulled_at
        FROM exchange_rates
        WHERE target_currency = 'PKR'
        ORDER BY pulled_at DESC
    """):
        print(row)


def main():
    conn = sqlite3.connect(DB_NAME)
    setup_database(conn)

    data = fetch_rates()
    store_rates(conn, data)
    run_sample_queries(conn)

    conn.close()
    print(f"\nDone. Your data lives in '{DB_NAME}' — a real file you can inspect,"
          f" query, or even open in DB Browser for SQLite.")


if __name__ == "__main__":
    main()
