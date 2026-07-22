import json
from pathlib import Path

from kafka import KafkaConsumer
from pydantic import ValidationError

from schema import RetailTransaction


KAFKA_TOPIC = "retail-transactions"
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


valid_count = 0
invalid_count = 0

QUARANTINE_FILE.parent.mkdir(parents=True, exist_ok=True)


for message in consumer:
    try:
        transaction = RetailTransaction(**message.value)

        print("Valid transaction:", transaction.invoice_no)
        valid_count += 1

    except ValidationError as error:
        invalid_record = {
            "message": message.value,
            "validation_error": str(error),
        }

        with QUARANTINE_FILE.open("a", encoding="utf-8") as file:
            file.write(json.dumps(invalid_record) + "\n")

        invalid_count += 1


consumer.close()

print("Consumer completed.")
print("Valid records:", valid_count)
print("Invalid records:", invalid_count)