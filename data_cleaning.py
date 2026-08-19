import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).parent / "data" / "processed"

nav_history = pd.read_csv(RAW_DIR / "02_nav_history.csv")
nav_history["date"] = pd.to_datetime(nav_history["date"])

nav_history = nav_history.sort_values(["amfi_code", "date"])

cleaned_groups = []

for code, group in nav_history.groupby("amfi_code"):
    group = group.set_index("date")
    full_range = pd.date_range(group.index.min(), group.index.max(), freq="D")
    group = group.reindex(full_range)
    group["nav"] = group["nav"].ffill()
    group["amfi_code"] = code
    group.index.name = "date"
    group = group.reset_index()
    cleaned_groups.append(group)

nav_history = pd.concat(cleaned_groups, ignore_index=True)

nav_history = nav_history.drop_duplicates()

invalid_nav_count = (nav_history["nav"] <= 0).sum()
print(f"Rows with NAV <= 0: {invalid_nav_count}")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
nav_history.to_csv(PROCESSED_DIR / "clean_nav_history.csv", index=False)
print(f"Saved cleaned NAV history: {len(nav_history)} rows")

# Task2: investor_transactions cleaning
transactions = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"])

invalid_amount_count = (transactions["amount_inr"] <= 0).sum()
print(f"Rows with amount_inr <= 0: {invalid_amount_count}")

transactions.to_csv(PROCESSED_DIR / "clean_transactions.csv", index=False)
print(f"Saved cleaned transactions: {len(transactions)} rows")

# Task3 : scheme_performance cleaning 
performance = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")

return_cols = ["return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "sharpe_ratio", "sortino_ratio"]
print(performance[return_cols].isnull().sum())

negative_sharpe = performance[performance["sharpe_ratio"] < 0]
print(f"\nFunds with negative Sharpe ratio: {len(negative_sharpe)}")
if len(negative_sharpe) > 0:
    print(negative_sharpe[["scheme_name", "sharpe_ratio"]])

out_of_range_expense = performance[(performance["expense_ratio_pct"] < 0.1) | (performance["expense_ratio_pct"] > 2.5)]
print(f"\nFunds with expense_ratio_pct outside 0.1%-2.5%: {len(out_of_range_expense)}")
if len(out_of_range_expense) > 0:
    print(out_of_range_expense[["scheme_name", "expense_ratio_pct"]])

performance.to_csv(PROCESSED_DIR / "clean_performance.csv", index=False)
print(f"\nSaved cleaned performance: {len(performance)} rows")