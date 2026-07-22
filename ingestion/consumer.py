import json
from pathlib import Path

import pandas as pd
from deltalake import write_deltalake
from kafka import KafkaConsumer
from pydantic import ValidationError

from schema import RetailTransaction


KAFKA_TOPIC = "retail-transactions"
BRONZE_PATH = Path("data/bronze/retail_transactions")
QUARANTINE_FILE = Path("data/quarantine/kafka_invalid_records.jsonl")


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    group_id="shopstream-consumer-group",
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    consumer_timeout_ms=5000,
)


valid_records = []
invalid_count = 0

QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)
BRONZE_PATH.parent.mkdir(parents=True, exist_ok=True)


for message in consumer:
    try:
        transaction = RetailTransaction(**message.value)

        valid_records.append(
            transaction.model_dump(mode="json")
        )

        print("Valid transaction:", transaction.invoice_no)

    except ValidationError as error:
        invalid_record = {
            "message": message.value,
            "validation_error": str(error),
        }

        with QUARANTINE_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(invalid_record) + "\n")

        invalid_count += 1


consumer.close()


if valid_records:
    bronze_df = pd.DataFrame(valid_records)

    write_deltalake(
        str(BRONZE_PATH),
        bronze_df,
        mode="append",
    )


print("Consumer completed.")
print("Valid records saved to Bronze:", len(valid_records))
print("Invalid records:", invalid_count)