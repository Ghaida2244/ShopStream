from datetime import datetime, timezone
from pathlib import Path

import great_expectations as gx
from deltalake import DeltaTable
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


SILVER_PATH = "data/silver/retail_transactions"
LINEAGE_FILE = "data/lineage/events.jsonl"
PRODUCER = "https://github.com/Ghaida2244/ShopStream"


Path(LINEAGE_FILE).parent.mkdir(parents=True, exist_ok=True)


file_config = FileConfig(
    log_file_path=LINEAGE_FILE,
    append=True,
)

lineage_client = OpenLineageClient(
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
    name="quality_check.passed",
)


def emit_lineage_event(event_state, outputs=None):
    event = RunEvent(
        eventType=event_state,
        eventTime=datetime.now(timezone.utc).isoformat(),
        run=run,
        job=job,
        producer=PRODUCER,
        inputs=[input_dataset],
        outputs=outputs or [],
    )

    lineage_client.emit(event)


emit_lineage_event(RunState.START)
print("START event emitted.")


try:
    silver_table = DeltaTable(SILVER_PATH)
    silver_df = silver_table.to_pandas()

    context = gx.get_context()

    data_source = context.data_sources.add_pandas(
        name="silver_pandas_source"
    )

    data_asset = data_source.add_dataframe_asset(
        name="silver_transactions"
    )

    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name="silver_batch"
    )

    batch = batch_definition.get_batch(
        batch_parameters={
            "dataframe": silver_df
        }
    )

    expectations = [
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=1
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="invoice_no"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="stock_code"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="country"
        ),
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="unit_price",
            min_value=0
        ),
        gx.expectations.ExpectColumnToExist(
            column="total_amount"
        ),
       
    ]

    all_checks_passed = True

    for expectation in expectations:
        result = batch.validate(expectation)

        expectation_name = expectation.__class__.__name__

        print(
            expectation_name,
            "passed:" if result.success else "failed:",
            result.success,
        )

        if not result.success:
            all_checks_passed = False

    if not all_checks_passed:
        raise ValueError("Silver data quality checks failed.")

    emit_lineage_event(
        RunState.COMPLETE,
        outputs=[output_dataset],
    )

    print("All Silver data quality checks passed.")
    print("COMPLETE event emitted.")

except Exception:
    emit_lineage_event(RunState.FAIL)
    print("FAIL event emitted.")
    raise