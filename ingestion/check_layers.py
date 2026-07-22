from deltalake import DeltaTable


BRONZE_PATH = "data/bronze/retail_transactions"
SILVER_PATH = "data/silver/retail_transactions"
GOLD_PATH = "data/gold/sales_by_country"


def check_table(name, path):
    table = DeltaTable(path)
    dataframe = table.to_pandas()

    print(f"{name} layer")
    print("Records:", len(dataframe))
    print("Columns:", len(dataframe.columns))
    print("-" * 30)


check_table("Bronze", BRONZE_PATH)
check_table("Silver", SILVER_PATH)
check_table("Gold", GOLD_PATH)