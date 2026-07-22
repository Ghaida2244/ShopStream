from pathlib import Path

import pandas as pd
from deltalake import DeltaTable, write_deltalake


BRONZE_PATH = Path("data/bronze/retail_transactions")
SILVER_PATH = Path("data/silver/retail_transactions")


bronze_table = DeltaTable(str(BRONZE_PATH))
silver_df = bronze_table.to_pandas()


silver_df["description"] = silver_df["description"].fillna("Unknown")
silver_df["country"] = silver_df["country"].str.strip()
silver_df["invoice_date"] = pd.to_datetime(silver_df["invoice_date"])

silver_df["total_amount"] = (
    silver_df["quantity"] * silver_df["unit_price"]
)


SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

write_deltalake(
    str(SILVER_PATH),
    silver_df,
    mode="overwrite",
)


print("Silver table created.")
print("Silver records:", len(silver_df))
print("Silver columns:", len(silver_df.columns))
print(silver_df.head())