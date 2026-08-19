-- 1. Top 5 funds by AUM
SELECT scheme_name, aum_crore FROM fact_performance ORDER BY aum_crore DESC LIMIT 5;

-- 2. Average NAV per month for HDFC Top 100 Direct
SELECT strftime('%Y-%m', date) AS month, AVG(nav) AS avg_nav
FROM fact_nav WHERE amfi_code = '125497' GROUP BY month;

-- 3. SIP inflow total by transaction type
SELECT transaction_type, SUM(amount_inr) AS total_amount, COUNT(*) AS num_transactions
FROM fact_transactions GROUP BY transaction_type;

-- 4. Transactions by state
SELECT state, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions GROUP BY state ORDER BY total_amount DESC;

-- 5. Funds with expense_ratio < 1%
SELECT scheme_name, expense_ratio_pct FROM dim_fund WHERE expense_ratio_pct < 1.0;

-- 6. Average Sharpe ratio by category
SELECT category, AVG(sharpe_ratio) AS avg_sharpe
FROM fact_performance GROUP BY category;

-- 7. Top 5 funds by 3-year return
SELECT scheme_name, return_3yr_pct FROM fact_performance ORDER BY return_3yr_pct DESC LIMIT 5;

-- 8. Fund houses with most schemes
SELECT fund_house, COUNT(*) AS num_schemes FROM dim_fund GROUP BY fund_house ORDER BY num_schemes DESC;

-- 9. Investor transaction count and total by age group
SELECT age_group, COUNT(*) AS num_transactions, SUM(amount_inr) AS total_amount
FROM fact_transactions GROUP BY age_group ORDER BY total_amount DESC;

-- 10. Join example: transactions with fund category
SELECT t.transaction_type, f.category, COUNT(*) AS num_transactions
FROM fact_transactions t
JOIN dim_fund f ON t.amfi_code = f.amfi_code
GROUP BY t.transaction_type, f.category;