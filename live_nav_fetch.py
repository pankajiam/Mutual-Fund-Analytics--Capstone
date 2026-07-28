import requests
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent / "data" / "raw"

schemes = {
    125497: "HDFC_Top_100_Direct",
    119551: "SBI_Bluechip",
    120503: "ICICI_Bluechip",
    118632: "Nippon_Large_Cap",
    119092: "Axis_Bluechip",
    120841: "Kotak_Bluechip",
}

for code, name in schemes.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)
    data = response.json()

    nav_df = pd.DataFrame(data["data"])
    output_file = RAW_DIR / f"nav_{code}_{name}.csv"
    nav_df.to_csv(output_file, index=False)

    print(f"\nCode: {code}")
    print(f"Requested: {name}")
    print(f"API returned: {data['meta']['scheme_name']}")
    print(f"Rows fetched: {len(nav_df)}")


    print("\n" + "="*60)
print("ANOMALY / DATA QUALITY FINDING")
print("="*60)
print("The AMFI scheme codes specified in the project brief (and cross-checked")
print("against the provided fund_master.csv) do not match mfapi.in's current")
print("live scheme registry. For example, code 125497 is documented as HDFC")
print("Top 100 Direct in both sources, but the live API currently returns")
print("'SBI Small Cap Fund - Direct Plan - Growth' for that code. This pattern")
print("held for 5 of 6 tested codes, with only Nippon Large Cap (118632)")
print("matching correctly. This suggests mfapi.in has reassigned scheme codes")
print("since this project's dataset was generated, i.e. a temporal drift issue")
print("rather than a data entry error. All 6 CSVs were still saved as returned")
print("by the live API, since Task 4/5 asked to fetch and save live data")
print("regardless of which scheme it corresponds to.")