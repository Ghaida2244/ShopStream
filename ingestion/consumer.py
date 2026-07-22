import json

from kafka import KafkaConsumer


KAFKA_TOPIC = "retail-transactions"


consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    value_deserializer=lambda value: json.loads(value.decode("utf-8")),
    consumer_timeout_ms=5000,
)


received_count = 0


for message in consumer:
    print(message.value)
    received_count += 1


consumer.close()

print("Consumer completed.")
print("Records received:", received_count)