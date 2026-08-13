# SQL Query Results

Executed against `data/processed/telco.db` (100,000 cleaned customer records).


## Q1. Overall churn rate
*What % of our customer base has churned?*

|   total_customers |   churned_customers |   churn_rate_pct |
|------------------:|--------------------:|-----------------:|
|            100000 |               33144 |            33.14 |


## Q2. Churn rate by contract type
*Does locking customers into longer contracts reduce churn?*

| Contract       |   customers |   churn_rate_pct |
|:---------------|------------:|-----------------:|
| Month-to-month |       54915 |            46.56 |
| Two year       |       19824 |            16.88 |
| One year       |       25261 |            16.75 |


## Q3. Churn rate by tenure group
*Is churn concentrated in new customers or long-standing ones?*

| TenureGroup   |   customers |   churn_rate_pct |
|:--------------|------------:|-----------------:|
| 0-1 yr        |       16647 |            64.01 |
| 1-2 yr        |       16637 |            26.87 |
| 2-4 yr        |       33332 |            26.86 |
| 4-6 yr        |       33384 |            27.16 |


## Q4. Churn rate by payment method
*Do certain payment methods correlate with higher churn (e.g. manual payment methods signaling lower engagement)?*

| PaymentMethod    |   customers |   churn_rate_pct |
|:-----------------|------------:|-----------------:|
| Mailed check     |       25221 |            33.33 |
| Electronic check |       34892 |            33.29 |
| Bank transfer    |       19855 |            33    |
| Credit card      |       20032 |            32.79 |


## Q5. Churn rate by gender and age group
*Are there demographic patterns worth targeting?*

| Gender   | AgeGroup   |   customers |   churn_rate_pct |
|:---------|:-----------|------------:|-----------------:|
| Female   | 18-25      |        6050 |            33.69 |
| Female   | 26-35      |        7635 |            33.61 |
| Female   | 36-45      |        7765 |            32.71 |
| Female   | 46-55      |        7655 |            32.91 |
| Female   | 56-65      |        7683 |            31.88 |
| Female   | 66-80      |       11468 |            32.6  |
| Male     | 18-25      |        6012 |            33.45 |
| Male     | 26-35      |        7663 |            32.74 |
| Male     | 36-45      |        7671 |            33.85 |
| Male     | 46-55      |        7443 |            34.29 |
| Male     | 56-65      |        7535 |            33.27 |
| Male     | 66-80      |       11463 |            32.96 |
| Other    | 18-25      |         512 |            35.35 |
| Other    | 26-35      |         638 |            31.82 |
| Other    | 36-45      |         620 |            35.97 |
| Other    | 46-55      |         624 |            33.97 |
| Other    | 56-65      |         610 |            35.25 |
| Other    | 66-80      |         953 |            32    |


## Q6. Average MonthlyCharges: churned vs retained customers
*Are we losing higher-value or lower-value customers?*

| Churn   |   customers |   avg_monthly_charges |   avg_total_charges |   avg_tenure_months |
|:--------|------------:|----------------------:|--------------------:|--------------------:|
| No      |       66856 |                 72.85 |             2886.13 |                39.3 |
| Yes     |       33144 |                 94.36 |             3007.43 |                30.9 |


## Q7. Revenue at risk: monthly recurring revenue currently churned
*What is the $ impact of churn on monthly recurring revenue?*

|   mrr_lost_to_churn |   total_mrr |   pct_mrr_lost |
|--------------------:|------------:|---------------:|
|         3.12731e+06 | 7.99749e+06 |           39.1 |


## Q8. Highest-risk segment: Month-to-month + first year tenure
*What does our single highest-risk, highest-priority retention segment look like, and how big is it?*

|   customers_in_segment |   churn_rate_pct |   mrr_at_risk_in_segment |
|-----------------------:|-----------------:|-------------------------:|
|                   9148 |            77.54 |                   608714 |


## Q9. Churn rate by MonthlyCharges quartile
*Does pricing tier relate to churn risk?*

|   charge_quartile |   min_charge |   max_charge |   customers |   churn_rate_pct |
|------------------:|-------------:|-------------:|------------:|-----------------:|
|                 1 |        10    |        44.72 |       25000 |            22.72 |
|                 2 |        44.72 |        80    |       25000 |            22.46 |
|                 3 |        80    |       115.05 |       25000 |            35.28 |
|                 4 |       115.05 |       150    |       25000 |            52.12 |


## Q10. Contract x Tenure interaction
*Does a long-term contract still reduce churn risk even for brand-new customers, or does tenure dominate regardless of contract?*

| Contract       | TenureGroup   |   customers |   churn_rate_pct |
|:---------------|:--------------|------------:|-----------------:|
| Month-to-month | 0-1 yr        |        9148 |            77.54 |
| Month-to-month | 1-2 yr        |        9085 |            40.45 |
| Month-to-month | 2-4 yr        |       18393 |            39.92 |
| Month-to-month | 4-6 yr        |       18289 |            40.77 |
| One year       | 0-1 yr        |        4190 |            47.42 |
| One year       | 1-2 yr        |        4192 |            10.16 |
| One year       | 2-4 yr        |        8456 |            10.6  |
| One year       | 4-6 yr        |        8423 |            10.95 |
| Two year       | 0-1 yr        |        3309 |            47.6  |
| Two year       | 1-2 yr        |        3360 |            11.01 |
| Two year       | 2-4 yr        |        6483 |            11.01 |
| Two year       | 4-6 yr        |        6672 |            10.3  |
