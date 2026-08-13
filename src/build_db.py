"""Loads the cleaned CSV into a SQLite database so sql/analysis_queries.sql
can be run directly against real data."""

import sqlite3
import pandas as pd

df = pd.read_csv("data/processed/telco_clean.csv")
conn = sqlite3.connect("data/processed/telco.db")
df.to_sql("customers", conn, if_exists="replace", index=False)
conn.close()
print(f"Loaded {len(df)} rows into data/processed/telco.db (table: customers)")
