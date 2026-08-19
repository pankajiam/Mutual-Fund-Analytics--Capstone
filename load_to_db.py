import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, text

PROCESSED_DIR = Path(__file__).parent / "data" / "processed"
RAW_DIR = Path(__file__).parent / "data" / "raw"
DB_PATH = Path(__file__).parent / "dashboard" / "bluestock_mf.db"

engine = create_engine(f"sqlite:///{DB_PATH}")

with open(Path(__file__).parent / "sql" / "schema.sql") as f:
    schema_sql = f.read()

with engine.connect() as conn:
    for statement in schema_sql.split(";"):
        if statement.strip():
            conn.execute(text(statement))
    conn.commit()

print("Schema created.")

fund_master = pd.read_csv(RAW_DIR / "01_fund_master.csv", dtype={"amfi_code": str})
nav_history = pd.read_csv(PROCESSED_DIR / "clean_nav_history.csv", dtype={"amfi_code": str})
transactions = pd.read_csv(PROCESSED_DIR / "clean_transactions.csv", dtype={"amfi_code": str})
performance = pd.read_csv(PROCESSED_DIR / "clean_performance.csv", dtype={"amfi_code": str})
aum = pd.read_csv(RAW_DIR / "03_aum_by_fund_house.csv")

fund_master.to_sql("dim_fund", engine, if_exists="append", index=False)
nav_history[["amfi_code", "date", "nav"]].to_sql("fact_nav", engine, if_exists="append", index=False)
transactions.to_sql("fact_transactions", engine, if_exists="append", index=False)
performance.to_sql("fact_performance", engine, if_exists="append", index=False)
aum.to_sql("fact_aum", engine, if_exists="append", index=False)

print(f"dim_fund: {len(fund_master)} rows loaded")
print(f"fact_nav: {len(nav_history)} rows loaded")
print(f"fact_transactions: {len(transactions)} rows loaded")
print(f"fact_performance: {len(performance)} rows loaded")
print(f"fact_aum: {len(aum)} rows loaded")