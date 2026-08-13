"""Runs each query in sql/analysis_queries.sql against the SQLite DB and
writes the results to reports/sql_query_results.md for reference in the
business report and README."""

import sqlite3
import re
import pandas as pd

with open("sql/analysis_queries.sql") as f:
    sql_text = f.read()

# Split into individual queries using the "-- Q<n>." markers as delimiters
blocks = re.split(r"(?=-- Q\d+\.)", sql_text)
blocks = [b.strip() for b in blocks if b.strip().startswith("-- Q")]

conn = sqlite3.connect("data/processed/telco.db")

output_lines = ["# SQL Query Results\n", "Executed against `data/processed/telco.db` (100,000 cleaned customer records).\n"]

for block in blocks:
    lines = block.split("\n")
    header_line = lines[0]  # -- Q1. Title
    query_title = header_line.replace("--", "").strip()

    # Business question may span multiple comment lines until the SELECT/WITH starts
    bq_parts = []
    capturing = False
    for l in lines[1:]:
        if "Business question:" in l:
            capturing = True
            bq_parts.append(l.split("Business question:")[1].strip())
        elif capturing and l.strip().startswith("--"):
            bq_parts.append(l.replace("--", "").strip())
        elif capturing:
            break
    business_q = " ".join(bq_parts).strip()

    query_sql = block
    try:
        df_result = pd.read_sql_query(query_sql, conn)
    except Exception as e:
        df_result = pd.DataFrame({"error": [str(e)]})

    output_lines.append(f"\n## {query_title}")
    if business_q:
        output_lines.append(f"*{business_q}*\n")
    output_lines.append(df_result.to_markdown(index=False))
    output_lines.append("")

conn.close()

with open("reports/sql_query_results.md", "w") as f:
    f.write("\n".join(output_lines))

print("Saved query results to reports/sql_query_results.md")
print("\n".join(output_lines[:40]))
