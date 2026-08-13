-- =====================================================================
-- analysis_queries.sql
-- Telco Customer Churn Analysis -- SQLite (data/processed/telco.db)
-- Table: customers (100,000 rows, post-cleaning)
-- =====================================================================

-- Q1. Overall churn rate
-- Business question: What % of our customer base has churned?
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers;


-- Q2. Churn rate by contract type
-- Business question: Does locking customers into longer contracts reduce churn?
SELECT
    Contract,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;


-- Q3. Churn rate by tenure group
-- Business question: Is churn concentrated in new customers or long-standing ones?
SELECT
    TenureGroup,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY TenureGroup
ORDER BY
    CASE TenureGroup
        WHEN '0-1 yr' THEN 1
        WHEN '1-2 yr' THEN 2
        WHEN '2-4 yr' THEN 3
        WHEN '4-6 yr' THEN 4
    END;


-- Q4. Churn rate by payment method
-- Business question: Do certain payment methods correlate with higher churn
-- (e.g. manual payment methods signaling lower engagement)?
SELECT
    PaymentMethod,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY PaymentMethod
ORDER BY churn_rate_pct DESC;


-- Q5. Churn rate by gender and age group
-- Business question: Are there demographic patterns worth targeting?
SELECT
    Gender,
    AgeGroup,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Gender, AgeGroup
ORDER BY Gender, AgeGroup;


-- Q6. Average MonthlyCharges: churned vs retained customers
-- Business question: Are we losing higher-value or lower-value customers?
SELECT
    Churn,
    COUNT(*) AS customers,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2) AS avg_total_charges,
    ROUND(AVG(Tenure), 1) AS avg_tenure_months
FROM customers
GROUP BY Churn;


-- Q7. Revenue at risk: monthly recurring revenue currently churned
-- Business question: What is the $ impact of churn on monthly recurring revenue?
SELECT
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_lost_to_churn,
    ROUND(SUM(MonthlyCharges), 2) AS total_mrr,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END) / SUM(MonthlyCharges), 2) AS pct_mrr_lost
FROM customers;


-- Q8. Highest-risk segment: Month-to-month + first year tenure
-- Business question: What does our single highest-risk, highest-priority
-- retention segment look like, and how big is it?
SELECT
    COUNT(*) AS customers_in_segment,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS mrr_at_risk_in_segment
FROM customers
WHERE Contract = 'Month-to-month' AND TenureGroup = '0-1 yr';


-- Q9. Churn rate by MonthlyCharges quartile
-- Business question: Does pricing tier relate to churn risk?
WITH quartiles AS (
    SELECT *,
        NTILE(4) OVER (ORDER BY MonthlyCharges) AS charge_quartile
    FROM customers
)
SELECT
    charge_quartile,
    ROUND(MIN(MonthlyCharges), 2) AS min_charge,
    ROUND(MAX(MonthlyCharges), 2) AS max_charge,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM quartiles
GROUP BY charge_quartile
ORDER BY charge_quartile;


-- Q10. Contract x Tenure interaction
-- Business question: Does a long-term contract still reduce churn risk even
-- for brand-new customers, or does tenure dominate regardless of contract?
SELECT
    Contract,
    TenureGroup,
    COUNT(*) AS customers,
    ROUND(100.0 * SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract, TenureGroup
ORDER BY Contract,
    CASE TenureGroup
        WHEN '0-1 yr' THEN 1
        WHEN '1-2 yr' THEN 2
        WHEN '2-4 yr' THEN 3
        WHEN '4-6 yr' THEN 4
    END;
