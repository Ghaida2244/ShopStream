from pathlib import Path

import pyarrow as pa
from deltalake import DeltaTable, write_deltalake


BRONZE_PATH = Path("data/bronze/retail_transactions")
SILVER_PATH = Path("data/silver/retail_transactions")


bronze_table = DeltaTable(str(BRONZE_PATH))
silver_df = bronze_table.to_pandas()


silver_df["description"] = silver_df["description"].fillna("Unknown")
silver_df["country"] = silver_df["country"].str.strip()
silver_df["invoice_date"] = silver_df["invoice_date"].astype(str)

silver_df["total_amount"] = (
    silver_df["quantity"] * silver_df["unit_price"]
)


SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)


if not SILVER_PATH.exists():
    write_deltalake(
        str(SILVER_PATH),
        silver_df,
        mode="overwrite",
    )

    print("Silver table created.")

else:
    silver_table = DeltaTable(str(SILVER_PATH))
    source_table = pa.Table.from_pandas(
        silver_df,
        preserve_index=False,
    )

    merge_result = (
        silver_table.merge(
            source=source_table,
            predicate=(
                "target.invoice_no = source.invoice_no "
                "AND target.stock_code = source.stock_code "
                "AND target.invoice_date = source.invoice_date"
            ),
            source_alias="source",
            target_alias="target",
        )
        .when_matched_update_all()
        .when_not_matched_insert_all()
        .execute()
    )

    print("Silver table updated using MERGE.")
    print("MERGE result:", merge_result)


updated_table = DeltaTable(str(SILVER_PATH))
updated_df = updated_table.to_pandas()

print("Silver records:", len(updated_df))
print("Silver columns:", len(updated_df.columns))