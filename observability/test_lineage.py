from pathlib import Path
from datetime import datetime, timezone

from openlineage.client import OpenLineageClient
from openlineage.client.event_v2 import (
    Dataset,
    Job,
    Run,
    RunEvent,
    RunState,
)
from openlineage.client.transport.file import FileConfig, FileTransport
from openlineage.client.uuid import generate_new_uuid


LINEAGE_FILE = "data/lineage/events.jsonl"
PRODUCER = "https://github.com/Ghaida2244/ShopStream"

Path(LINEAGE_FILE).parent.mkdir(parents=True, exist_ok=True)


file_config = FileConfig(
    log_file_path=LINEAGE_FILE,
    append=True,
)

client = OpenLineageClient(
    transport=FileTransport(file_config)
)


job = Job(
    namespace="shopstream",
    name="silver_quality_check",
)

run = Run(
    runId=str(generate_new_uuid())
)

input_dataset = Dataset(
    namespace="shopstream",
    name="silver.retail_transactions",
)

output_dataset = Dataset(
    namespace="shopstream",
    name="quality_check.result",
)


start_event = RunEvent(
    eventType=RunState.START,
    eventTime=datetime.now(timezone.utc).isoformat(),
    run=run,
    job=job,
    producer=PRODUCER,
    inputs=[input_dataset],
)

client.emit(start_event)

print("START event emitted.")


complete_event = RunEvent(
    eventType=RunState.COMPLETE,
    eventTime=datetime.now(timezone.utc).isoformat(),
    run=run,
    job=job,
    producer=PRODUCER,
    inputs=[input_dataset],
    outputs=[output_dataset],
)

client.emit(complete_event)

print("COMPLETE event emitted.")