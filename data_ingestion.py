import pandas as pd 
from pathlib import Path

RAW_DIR = Path(__file__).parent/ "data"/"raw"

csv_files = sorted(RAW_DIR.glob("*.csv"))

for file_path in csv_files:
    df = pd.read_csv(file_path)
    print(f"\n{'='*60}")
    print(f"FILE: {file_path.name}")
    print(f"{'='*60}")
    print(f"Shape: {df.shape}")
    print(f"\nDtypes:\n{df.dtypes}")
    print(f"\nHead:\n{df.head()}")

    print("\n\nANOMALY NOTES:")
print("- amfi_code loads as int64 (number) in multiple files, though it's really an ID/code, not a quantity. Should likely be treated as text in Day 2 cleaning, to avoid issues like dropped leading zeros.")
print("- 04_monthly_sip_inflows.csv: yoy_growth_pct is NaN for the first 12 months (Jan-Dec 2022), because there's no prior-year (2021) data to compare against. This is expected, not an error.")

fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv")

print("\n" + "="*60)
print("FUND MASTER EXPLORATION")
print("="*60)

print("\nUnique fund houses:")
print(fund_master["fund_house"].unique())

print("\nUnique categories:")
print(fund_master["category"].unique())

print("\nUnique sub-categories:")
print(fund_master["sub_category"].unique())

print("\nUnique risk categories:")
print(fund_master["risk_category"].unique())

nav_history = pd.read_csv(RAW_DIR / "02_nav_history.csv")

master_codes = set(fund_master["amfi_code"].unique())
nav_codes = set(nav_history["amfi_code"].unique())

missing_codes = master_codes - nav_codes

print("\n" + "="*60)
print("AMFI CODE VALIDATION — DATA QUALITY SUMMARY")
print("="*60)
print(f"Total unique codes in fund_master: {len(master_codes)}")
print(f"Total unique codes in nav_history: {len(nav_codes)}")
print(f"Codes in fund_master but missing from nav_history: {len(missing_codes)}")

if missing_codes:
    print(f"Missing codes: {missing_codes}")
else:
    print("All fund_master codes have matching NAV history. No gaps found.")


summary_text = """
DAY 1 — DATA QUALITY SUMMARY
==============================

ANOMALIES FOUND:
1. amfi_code loads as int64 (number) across multiple files, though it is
   really an ID/code, not a quantity. Recommend treating as text/string
   in Day 2 cleaning, to avoid risks like dropped leading zeros.

2. 04_monthly_sip_inflows.csv: yoy_growth_pct is NaN for the first 12
   months (Jan-Dec 2022). This is expected, not an error, since no
   prior-year (2021) data exists in this dataset to compare against.

3. fund_master.csv contains only 'Equity' and 'Debt' categories, despite
   the project's business context mentioning Hybrid schemes as well.

AMFI CODE VALIDATION:
- Total unique codes in fund_master: 40
- Total unique codes in nav_history: 40
- Missing codes: 0 (all fund_master codes have matching NAV history)

LIVE API FINDING (mfapi.in):
- AMFI scheme codes referenced in the project brief (and confirmed
  against fund_master.csv) do not match mfapi.in's current live
  registry. 5 of 6 tested codes returned unrelated funds. Only Nippon
  Large Cap (118632) matched correctly. This points to a drift in
  mfapi.in's scheme code mapping since this project's dataset was
  generated, not a data entry error on our side. Live data was still
  fetched and saved as returned by the API.
"""

report_path = Path(__file__).parent / "reports" / "day1_data_quality_summary.txt"
with open(report_path, "w") as f:
    f.write(summary_text)

print(f"\nData quality summary saved to: {report_path}")