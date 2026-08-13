# Telco Customer Churn Prediction

Predicting and explaining customer churn for a telecom-style business using
SQL, Python, and machine learning — with an emphasis on business
recommendations, not just model accuracy.

## Business Question

Which customers are most likely to churn, and where should retention
spend be prioritized to reduce revenue loss?

## Headline Finding

**Churn is not evenly spread across the customer base.** Month-to-month
customers in their first year of tenure churn at **77.5%**, versus an
overall churn rate of 33.1%. That segment alone represents **$608,714/month**
in at-risk recurring revenue. Contract type and tenure — not demographics —
are the dominant drivers of churn. Full findings: [`reports/business_report.md`](reports/business_report.md).

## Dataset

`data/raw/synthetic_customer_churn_100k.csv` — 100,000 customer records,
9 columns (CustomerID, Age, Gender, Tenure, MonthlyCharges, Contract,
PaymentMethod, TotalCharges, Churn).

## Repository Structure

```
telco-customer-churn-prediction/
│
├── data/
│   ├── raw/                  # Original uploaded dataset
│   └── processed/            # Cleaned CSV + SQLite database
├── sql/
│   └── analysis_queries.sql  # 10 business-framed SQL queries
├── src/
│   ├── data_cleaning.py      # Cleaning logic, decisions documented inline
│   ├── build_db.py           # Loads cleaned data into SQLite
│   ├── run_sql_queries.py    # Executes all SQL queries, saves results
│   ├── eda.py                 # Generates all charts in images/
│   ├── model.py                # Trains + evaluates churn models
│   └── build_notebook.py     # Programmatically builds the notebook
├── notebook/
│   └── telco_churn_analysis.ipynb   # Full analysis, executed with real outputs
├── images/                   # All charts (7 EDA + 3 model charts)
├── reports/
│   ├── business_report.md    # Findings, recommendations, limitations
│   ├── sql_query_results.md  # All 10 SQL query outputs
│   └── model_metrics.csv     # Model comparison table
├── docs/
├── requirement.txt
└── README.md
```

## How to Reproduce

```bash
pip install -r requirement.txt

python3 src/data_cleaning.py     # cleans raw data -> data/processed/telco_clean.csv
python3 src/build_db.py          # builds SQLite db -> data/processed/telco.db
python3 src/run_sql_queries.py   # runs sql/analysis_queries.sql -> reports/sql_query_results.md
python3 src/eda.py               # generates charts -> images/
python3 src/model.py             # trains models -> reports/model_metrics.csv, images/
```

Or open `notebook/telco_churn_analysis.ipynb` for the full narrative walkthrough.

## Methodology

1. **Data cleaning** — 265 records (0.27%) had negative `TotalCharges`
   (a data quality error, since billed amounts can't be negative).
   Reconstructed from `Tenure × MonthlyCharges` rather than dropped, since
   the two correlate at 0.9998 in valid rows. Full reasoning documented in
   `src/data_cleaning.py`.
2. **SQL analysis** — 10 business-framed queries covering churn rate by
   contract, tenure, payment method, demographics, pricing quartile, and a
   segment-level revenue-at-risk calculation.
3. **EDA** — visualized every relationship found in SQL, plus a
   contract × tenure interaction heatmap and a correlation matrix.
4. **Modeling** — Logistic Regression (interpretable baseline) and Random
   Forest (ROC-AUC 0.806), with feature importance used to independently
   verify the SQL/EDA findings rather than replace them.
5. **Business report** — translates findings into four concrete
   recommendations, and is explicit about what the data *doesn't* support
   (e.g. no causal claim on the price–churn relationship).

## Key Results

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 72.3% | 60.8% | 46.6% | 52.8% | 0.772 |
| Random Forest | 76.2% | 66.9% | 56.0% | 61.0% | **0.806** |

**Top churn drivers (Random Forest feature importance):** MonthlyCharges (32%),
Tenure (28%), Contract type (30% combined) — together ~89% of predictive
weight. Age, Gender, and PaymentMethod combined: <2%.

## Tech Stack

Python (pandas, scikit-learn, matplotlib, seaborn) · SQL (SQLite) · Jupyter

## What I'd Do Next

- Test a retention offer on the month-to-month/first-year segment and
  measure the before/after churn rate.
- Add service-usage or support-ticket data if available — the model's
  recall (56%) suggests there's more churn signal not captured by
  demographic/billing fields alone.
- Re-train the model quarterly as new cohorts age into the 1-2yr tenure bucket.
