import pandas as pd

file_path = "data/raw/online_retail.csv"

df = pd.read_csv(file_path)

print(df.head())
print("Number of rows:", df.shape[0])
print("Number of columns:", df.shape[1])