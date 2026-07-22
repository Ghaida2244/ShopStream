from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from schema import RetailTransaction


input_file = Path("data/raw/online_retail.csv")
quarantine_file = Path("data/quarantine/invalid_records.csv")

df = pd.read_csv(input_file)

valid_count = 0
invalid_records = []


for _, row in df.iterrows():
    transaction = {
        "invoice_no": str(row["InvoiceNo"]),
        "stock_code": str(row["StockCode"]),
        "description": (
            None if pd.isna(row["Description"]) else str(row["Description"])
        ),
        "quantity": row["Quantity"],
        "invoice_date": row["InvoiceDate"],
        "unit_price": row["UnitPrice"],
        "customer_id": (
            None if pd.isna(row["CustomerID"]) else row["CustomerID"]
        ),
        "country": str(row["Country"]),
    }

    try:
        RetailTransaction(**transaction)
        valid_count += 1

    except ValidationError as error:
        invalid_record = row.to_dict()
        invalid_record["validation_error"] = str(error)
        invalid_records.append(invalid_record)


quarantine_file.parent.mkdir(parents=True, exist_ok=True)

if invalid_records:
    pd.DataFrame(invalid_records).to_csv(quarantine_file, index=False)


print("Validation completed.")
print("Valid records:", valid_count)
print("Invalid records:", len(invalid_records))
print("Total records:", len(df))