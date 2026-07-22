from deltalake import DeltaTable


BRONZE_PATH = "data/bronze/retail_transactions"


bronze_table = DeltaTable(BRONZE_PATH)

bronze_df = bronze_table.to_pandas()

print(bronze_df.head())
print("Bronze records:", len(bronze_df))
print("Bronze columns:", len(bronze_df.columns))
