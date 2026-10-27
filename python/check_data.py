
import pandas as pd
from pathlib import Path

# Locate the project folder
project_folder = Path(__file__).resolve().parent.parent

# Locate the Excel file
file_path = project_folder / "data" / "Shopify Sales.xlsx"

# Read the sales data
df = pd.read_excel(file_path)

# Display the results
print("=" * 40)
print("SHOPIFY SALES ANALYSIS")
print("=" * 40)

print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())

print("\nMissing values:")
print(df.isnull().sum())

print("\nFirst 5 records:")
print(df.head())
