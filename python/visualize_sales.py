
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Find the project folders
project_folder = Path(__file__).resolve().parent.parent
data_file = project_folder / "data" / "shopify_cleaned.csv"
report_folder = project_folder / "reports"

# Create reports folder if needed
report_folder.mkdir(parents=True, exist_ok=True)

# Load the cleaned data
df = pd.read_csv(data_file)

# Convert sales and quantity columns to numbers
df["Total Price Usd"] = pd.to_numeric(
    df["Total Price Usd"], errors="coerce"
)
df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
)

# Chart 1: Revenue by product type
product_sales = (
    df.groupby("Product Type")["Total Price Usd"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(10, 6))
product_sales.sort_values().plot(kind="barh")
plt.title("Top 10 Product Types by Revenue")
plt.xlabel("Revenue (USD)")
plt.ylabel("Product Type")
plt.tight_layout()
plt.savefig(report_folder / "revenue_by_product.png", dpi=150)
plt.close()

# Chart 2: Monthly sales trend
df["Invoice Date"] = pd.to_datetime(
    df["Invoice Date"], errors="coerce"
)

monthly_sales = (
    df.dropna(subset=["Invoice Date"])
    .set_index("Invoice Date")["Total Price Usd"]
    .resample("MS")
    .sum()
)

plt.figure(figsize=(10, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Shopify Sales Trend")
plt.xlabel("Month")
plt.ylabel("Revenue (USD)")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(report_folder / "monthly_sales_trend.png", dpi=150)
plt.close()

print("Sales charts created successfully!")
print("Saved charts in:", report_folder)
print("- revenue_by_product.png")
print("- monthly_sales_trend.png")
