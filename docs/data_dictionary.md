# Data Dictionary

Source file: `data/raw/synthetic_customer_churn_100k.csv`

| Column | Type | Description |
|---|---|---|
| CustomerID | Integer | Unique customer identifier. Not used as a model feature. |
| Age | Integer | Customer age in years (range: 18-80). |
| Gender | Categorical | Male / Female / Other. |
| Tenure | Integer | Months the customer has been with the company (range: 1-72). |
| MonthlyCharges | Float | Current monthly billed amount in $ (range: $10-$150). |
| Contract | Categorical | Month-to-month / One year / Two year. |
| PaymentMethod | Categorical | Electronic check / Mailed check / Bank transfer / Credit card. |
| TotalCharges | Float | Cumulative amount billed to date in $. 265 records had invalid negative values, corrected in cleaning — see `src/data_cleaning.py`. |
| Churn | Categorical | Yes / No — whether the customer has churned. Target variable. |

## Derived Columns (added during cleaning, `src/data_cleaning.py`)

| Column | Description |
|---|---|
| TenureGroup | Bucketed tenure: 0-1 yr / 1-2 yr / 2-4 yr / 4-6 yr |
| AgeGroup | Bucketed age: 18-25 / 26-35 / 36-45 / 46-55 / 56-65 / 66-80 |
| ChurnFlag | Churn recoded as 1/0 for modeling and aggregate calculations |
