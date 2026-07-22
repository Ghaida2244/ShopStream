import great_expectations as gx
from deltalake import DeltaTable


SILVER_PATH = "data/silver/retail_transactions"


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


print("All Silver data quality checks passed.")