# Telco Customer Churn — Business Report

**Prepared by:** Siddarth Nayak
**Dataset:** `synthetic_customer_churn_100k.csv` — 100,000 customer records
**Tools used:** Python (pandas, scikit-learn), SQL (SQLite), Power BI–style visualization via matplotlib/seaborn

---

## 1. Business Question

Which customers are most likely to churn, and what should the business
prioritize to reduce revenue loss from churn?

## 2. Headline Numbers

| Metric | Value |
|---|---|
| Total customers | 100,000 |
| Overall churn rate | 33.14% |
| Monthly recurring revenue (MRR) currently lost to churned customers | **$3,127,310** (39.1% of total MRR) |
| Highest-risk segment size | 9,148 customers (Month-to-month contract, <1 year tenure) |
| Churn rate in that segment | **77.5%** |
| MRR at risk in that segment alone | $608,714/month |

The single highest-risk, highest-priority segment — new customers on
month-to-month contracts — is only 9.1% of the customer base but accounts
for a disproportionate share of churn and revenue risk. This is where
retention spend should be concentrated first.

## 3. What Actually Drives Churn (and what doesn't)

Three independent methods — SQL group-bys, EDA visualizations, and a
Random Forest's feature importances — all agree on the same three drivers,
which gives real confidence in the finding rather than it being an
artifact of one method:

**Drives churn, ranked by impact:**
1. **Contract type** — Month-to-month customers churn at 46.6%, vs. 16.8%
   for One-year and Two-year contracts (see `images/churn_by_contract.png`).
2. **Tenure** — First-year customers churn at 64.0%, dropping to ~27% after
   year one and staying flat from there (`images/churn_by_tenure.png`).
   Most of the churn risk is concentrated in the *first 12 months*, not
   spread evenly across a customer's lifetime.
3. **Monthly charges** — Customers in the top pricing quartile ($115–$150/mo)
   churn at 52.1%, more than double the bottom two quartiles (~22.5%)
   (`images/churn_by_charge_quartile.png`). Churned customers also pay
   $21.51/month more on average than retained customers ($94.36 vs $72.85).

**The interaction matters more than any single factor.** The heatmap
(`images/churn_heatmap_contract_tenure.png`) shows contract type and
tenure compound each other: a brand-new month-to-month customer churns at
77.5%, but a brand-new customer on a one- or two-year contract already
churns at ~47% in year one — the contract alone doesn't protect a new
customer, tenure still has to build up.

**Does NOT meaningfully drive churn** (confirmed by both SQL breakdowns and
the model's near-zero feature importance):
- **Gender** — churn rate is flat across Male/Female/Other (32.6%–33.9%).
- **Age** — flat across all age groups (31.9%–34.3%).
- **Payment method** — flat across all four methods (32.8%–33.3%).

This is a useful negative finding, not a null result: it means retention
campaigns segmented by demographics or payment method will not be
effective, and that budget is better spent on contract- and tenure-based
targeting instead.

## 4. Predictive Model

Two models were built to test whether churn is predictable ahead of time
(see `src/model.py`, `reports/model_metrics.csv`):

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression (baseline) | 72.3% | 60.8% | 46.6% | 52.8% | 0.772 |
| Random Forest | 76.2% | 66.9% | 56.0% | 61.0% | **0.806** |

The Random Forest is the stronger model (ROC-AUC 0.806) and its feature
importances independently confirm the SQL/EDA findings: MonthlyCharges,
Tenure, and Contract type account for ~89% of the model's total predictive
weight combined, while Age, Gender, and PaymentMethod together account for
under 2%.

**Practical use:** a model like this could be run monthly to score active
customers and flag the top-decile churn-risk customers for proactive
retention outreach, rather than waiting to react after cancellation.

## 5. Recommendations

1. **Prioritize the month-to-month + first-year segment first.** It's the
   single highest-risk, highest-revenue-impact group ($608K/month at risk).
   A targeted incentive to convert these customers to a 1-year contract
   within their first 90 days would likely have the largest ROI of any
   retention action available.
2. **Front-load retention effort into month 1–12, not spread evenly.**
   Since churn risk drops sharply after year one regardless of contract
   type, a single well-timed intervention early in the relationship (e.g.
   an onboarding check-in, an early-tenure discount) is likely more
   effective than steady-state retention spend later.
3. **Investigate the high-monthly-charge churn link before assuming it's
   price sensitivity.** Top-quartile payers churn at more than double the
   bottom two quartiles. This report treats that as a flag for further
   investigation — e.g. via a customer survey or support-ticket review —
   rather than a conclusion, since the "why" behind it isn't visible in
   this dataset alone (see Limitations).
4. **Deprioritize demographic-based retention segmentation.** Gender, age,
   and payment method show no meaningful relationship to churn here —
   spending retention budget segmenting by these factors is unlikely to
   outperform simply targeting by contract type and tenure.

## 6. Limitations & What I'd Do Next

- **Data quality:** 265 records (0.27%) had negative `TotalCharges`,
  reconstructed from `Tenure × MonthlyCharges` (documented in
  `src/data_cleaning.py`). This is a small share of the data, but a
  real deployment would need to trace *why* the export produced negative
  values in the first place.
- **No service/product features available.** Unlike some churn datasets,
  this one has no internet type, add-on services, or support-ticket
  history. That likely caps the model's ceiling — the top features
  explain a lot but recall is still only 56%, meaning the model still
  misses a substantial share of churners. Adding service-usage or
  support-interaction data would likely improve this meaningfully.
- **No causal claims.** The high-monthly-charge → high-churn link is
  correlational. It could reflect price sensitivity, but it could equally
  reflect that high-paying customers use premium/complex plans with more
  to go wrong. This report intentionally stops at flagging it rather than
  asserting a cause.
- **Next steps if this were a live business problem:** run a controlled
  retention offer test on the month-to-month/first-year segment, track a
  before/after churn rate, and feed the results back into re-training the
  model quarterly.
