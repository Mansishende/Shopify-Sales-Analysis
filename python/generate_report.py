
import pandas as pd
from pathlib import Path

# Find project folders
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "shopify_cleaned.csv"
report_folder = project_folder / "reports"
report_folder.mkdir(parents=True, exist_ok=True)

# Load cleaned data
df = pd.read_csv(data_file)

# Prepare numeric columns
df["Total Price Usd"] = pd.to_numeric(
    df["Total Price Usd"], errors="coerce"
)
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

# Calculate sales figures
revenue = df["Total Price Usd"].sum()
orders = df["Order Number"].nunique()
customers = df["Customer Id"].nunique()
units_sold = df["Quantity"].sum()
average_order_value = revenue / orders if orders else 0

# Create report text
report = f"""
SHOPIFY SALES ANALYSIS REPORT
=============================

Total records: {len(df):,}
Total Revenue: ${revenue:,.2f} USD
Unique Orders: {orders:,}
Unique Customers: {customers:,}
Units Sold: {units_sold:,.0f}
Average Order Value: ${average_order_value:,.2f} USD

Note: Revenue and average order value are calculated
from the Total Price Usd column and unique order numbers.
"""

# Save report
report_file = report_folder / "sales_summary.txt"
report_file.write_text(report, encoding="utf-8")

print(report)
print("Report saved to:", report_file)
