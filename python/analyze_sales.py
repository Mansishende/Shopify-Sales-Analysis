
import pandas as pd
from pathlib import Path

# Find the project folder automatically
PROJECT_FOLDER = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_FOLDER / "data" / "shopify_cleaned.csv"

# Load the cleaned Shopify data
df = pd.read_csv(DATA_FILE)

print("\n===== SHOPIFY SALES ANALYSIS =====")
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

# Calculate sales KPIs
revenue = pd.to_numeric(
    df["Total Price Usd"], errors="coerce"
).sum()

orders = df["Order Number"].nunique()

customers = df["Customer Id"].nunique()

quantity = pd.to_numeric(
    df["Quantity"], errors="coerce"
).sum()

average_order_value = revenue / orders if orders else 0

# Display the results
print("\n===== SALES SUMMARY =====")
print(f"Total Revenue: ${revenue:,.2f} USD")
print(f"Total Orders: {orders:,}")
print(f"Unique Customers: {customers:,}")
print(f"Total Quantity Sold: {quantity:,.0f}")
print(f"Average Order Value: ${average_order_value:,.2f} USD")

print("\nAnalysis completed successfully!")
