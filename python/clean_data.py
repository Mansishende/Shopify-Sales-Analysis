
import pandas as pd
from pathlib import Path

# Locate project folders
project_folder = Path(__file__).resolve().parent.parent
input_file = project_folder / "data" / "Shopify Sales.xlsx"
output_file = project_folder / "data" / "shopify_cleaned.csv"

# Load the Excel file
df = pd.read_excel(input_file)

print("Original rows:", len(df))

# Remove completely duplicated rows
df = df.drop_duplicates()

# Remove spaces from column names
df.columns = df.columns.str.strip()

# Standardise text columns
for column in df.select_dtypes(include="object").columns:
    df[column] = df[column].map(
        lambda value: value.strip() if isinstance(value, str) else value
    )

# Save the cleaned data
df.to_csv(output_file, index=False)

print("Cleaned rows:", len(df))
print("Remaining duplicate rows:", df.duplicated().sum())
print("Cleaned file saved to:", output_file)
print("\nData cleaning completed successfully!")
