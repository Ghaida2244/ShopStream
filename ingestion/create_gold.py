from pathlib import Path

from deltalake import DeltaTable, write_deltalake


SILVER_PATH = Path("data/silver/retail_transactions")
GOLD_PATH = Path("data/gold/sales_by_country")


silver_table = DeltaTable(str(SILVER_PATH))
silver_df = silver_table.to_pandas()


gold_df = (
    silver_df.groupby("country", as_index=False)
    .agg(
        total_quantity=("quantity", "sum"),
        total_sales=("total_amount", "sum"),
        transaction_count=("invoice_no", "count"),
    )
    .sort_values("total_sales", ascending=False)
)


GOLD_PATH.parent.mkdir(parents=True, exist_ok=True)

write_deltalake(
    str(GOLD_PATH),
    gold_df,
    mode="overwrite",
)


print("Gold table created.")
print("Gold records:", len(gold_df))
print("Gold columns:", len(gold_df.columns))
print(gold_df.head())