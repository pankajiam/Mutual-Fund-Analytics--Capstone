# Data Dictionary — Bluestock MF Capstone

## dim_fund
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT (PK) | Unique AMFI scheme code |
| fund_house | TEXT | AMC name |
| scheme_name | TEXT | Full scheme name |
| category | TEXT | Equity / Debt |
| sub_category | TEXT | Large Cap, Small Cap, etc. |
| plan | TEXT | Regular or Direct |
| launch_date | TEXT | Fund launch date |
| benchmark | TEXT | Benchmark index |
| expense_ratio_pct | REAL | Annual expense ratio % |
| exit_load_pct | REAL | Exit load % |
| min_sip_amount | INTEGER | Minimum SIP investment (INR) |
| min_lumpsum_amount | INTEGER | Minimum lumpsum investment (INR) |
| fund_manager | TEXT | Fund manager name |
| risk_category | TEXT | SEBI risk level |
| sebi_category_code | TEXT | Internal SEBI code |

## fact_nav
| Column | Type | Description |
|---|---|---|
| nav_id | INTEGER (PK) | Auto-generated row ID |
| amfi_code | TEXT (FK → dim_fund) | Fund this NAV belongs to |
| date | TEXT | NAV date (forward-filled for weekends/holidays) |
| nav | REAL | Net Asset Value (INR) |

## fact_transactions
| Column | Type | Description |
|---|---|---|
| transaction_id | INTEGER (PK) | Auto-generated row ID |
| investor_id | TEXT | Investor identifier |
| transaction_date | TEXT | Date of transaction |
| amfi_code | TEXT (FK → dim_fund) | Fund involved |
| transaction_type | TEXT | SIP / Lumpsum / Redemption |
| amount_inr | INTEGER | Transaction amount |
| state, city, city_tier | TEXT | Investor location |
| age_group, gender, annual_income_lakh | — | Investor demographics |
| payment_mode | TEXT | UPI / Net Banking / etc. |
| kyc_status | TEXT | Verified / Pending |

## fact_performance
| Column | Type | Description |
|---|---|---|
| amfi_code | TEXT (PK, FK → dim_fund) | Fund identifier |
| return_1yr_pct, return_3yr_pct, return_5yr_pct | REAL | Returns over periods |
| sharpe_ratio, sortino_ratio | REAL | Risk-adjusted return metrics |
| alpha, beta | REAL | Benchmark-relative metrics |
| max_drawdown_pct | REAL | Worst peak-to-trough decline |
| expense_ratio_pct | REAL | Annual expense ratio |

## fact_aum
| Column | Type | Description |
|---|---|---|
| aum_id | INTEGER (PK) | Auto-generated row ID |
| date | TEXT | Quarter-end date |
| fund_house | TEXT | AMC name |
| aum_crore | INTEGER | Assets under management (Rs. crore) |
| num_schemes | INTEGER | Number of schemes under this AMC |

**Source:** All data provided by Bluestock Fintech, based on AMFI India public data and mfapi.in. Cleaned and loaded via `data_cleaning.py` and `load_to_db.py`.