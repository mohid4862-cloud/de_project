# Currency ETL Pipeline with dbt

An end-to-end data engineering project that extracts currency exchange rate data, loads it into a database, and transforms it into analytics-ready tables using dbt.

## Overview

This project demonstrates a full ETL (Extract, Transform, Load) workflow:

1. **Extract** — Pulls live currency exchange rate data from a free exchange rate API.
2. **Load** — Stores raw data in a local SQLite database.
3. **Transform** — Uses dbt to build a chain of models that clean, filter, and summarize the data into a final report.
4. **Automate** — Scheduled to run automatically using Windows Task Scheduler.

## Tech Stack

- **Python** — data extraction, cleaning, and loading scripts
- **SQLite** — lightweight local database for storing raw and processed data
- **dbt (data build tool)** — SQL-based transformation layer
- **Windows Task Scheduler** — automation/orchestration
- **Google BigQuery** — (optional) cloud upload for scaled analytics

## Project Structure
