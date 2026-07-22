import json
from pathlib import Path

import pandas as pd
from kafka import KafkaProducer
from pydantic import ValidationError

from schema import RetailTransaction


DATA_FILE = Path("data/raw/online_retail.csv")
KAFKA_TOPIC = "retail-transactions"


producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda value: json.dumps(value).encode("utf-8"),
)


df = pd.read_csv(DATA_FILE)

sent_count = 0
invalid_count = 0


for _, row in df.head(10).iterrows():
    transaction_data = {
        "invoice_no": str(row["InvoiceNo"]),
        "stock_code": str(row["StockCode"]),
        "description": (
            None if pd.isna(row["Description"]) else str(row["Description"])
        ),
        "quantity": int(row["Quantity"]),
        "invoice_date": str(row["InvoiceDate"]),
        "unit_price": float(row["UnitPrice"]),
        "customer_id": (
            None if pd.isna(row["CustomerID"]) else float(row["CustomerID"])
        ),
        "country": str(row["Country"]),
    }

    try:
        transaction = RetailTransaction(**transaction_data)

        producer.send(
            KAFKA_TOPIC,
            value=transaction.model_dump(mode="json"),
        )

        sent_count += 1

    except ValidationError as error:
        invalid_count += 1
        print("Invalid transaction:", error)


invalid_transaction = {
    "invoice_no": "TEST-INVALID",
    "stock_code": "TEST",
    "description": "Invalid test record",
    "quantity": 1,
    "invoice_date": "2010-12-01 08:26:00",
    "unit_price": -5.0,
    "customer_id": None,
    "country": "United Kingdom",
}

producer.send(
    KAFKA_TOPIC,
    value=invalid_transaction,
)


producer.flush()
producer.close()

print("Producer completed.")
print("Valid records sent:", sent_count)
print("Invalid test record sent: 1")