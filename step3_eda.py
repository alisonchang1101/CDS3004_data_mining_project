
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# 1. Set paths
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "outputs" / "step2_preliminary_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# 2. Load cleaned data
df = pd.read_csv(DATA_PATH)
df["Date"] = pd.to_datetime(df["Date"], errors="raise")

# 3. Prepare customer-level data
customer_summary = df.groupby("Customer_ID").agg(
    Total_Spending=("Total_Amount", "sum"),
    Purchase_Frequency=("Order_ID", "nunique")
).reset_index()

# 4. Basic statistics
print("=== CUSTOMER SUMMARY ===")
print("Total Customers:", len(customer_summary))
print("\nCustomer Spending Statistics:")
print(customer_summary["Total_Spending"].describe())
print("\nPurchase Frequency Statistics:")
print(customer_summary["Purchase_Frequency"].describe())

# 5. Chart 1: Customer Spending Distribution
plt.figure(figsize=(9, 5))
sns.histplot(
    customer_summary["Total_Spending"],
    bins=40,
    color="steelblue"
)
plt.title("Customer Spending Distribution")
plt.xlabel("Total Spending")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "step3_customer_spending.png",
    dpi=300
)
plt.close()

# 6. Chart 2: Purchase Frequency Distribution
plt.figure(figsize=(9, 5))
sns.histplot(
    customer_summary["Purchase_Frequency"],
    discrete=True,
    color="darkorange"
)
plt.title("Purchase Frequency Distribution")
plt.xlabel("Number of Orders")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "step3_purchase_frequency.png",
    dpi=300
)
plt.close()

# 7. Chart 3: Sales by Product Category
category_sales = (
    df.groupby("Product_Category")["Total_Amount"]
    .sum()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 5))
sns.barplot(
    x=category_sales.index,
    y=category_sales.values,
    color="steelblue"
)
plt.title("Sales by Product Category")
plt.xlabel("Product Category")
plt.ylabel("Total Sales")
plt.xticks(rotation=35, ha="right")
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "step3_category_sales.png",
    dpi=300
)
plt.close()

# 8. Chart 4: Monthly Sales Trend
monthly_sales = (
    df.set_index("Date")
    .resample("MS")["Total_Amount"]
    .sum()
)

plt.figure(figsize=(10, 5))
plt.plot(
    monthly_sales.index,
    monthly_sales.values,
    marker="o"
)
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=35)
plt.tight_layout()
plt.savefig(
    OUTPUT_DIR / "step3_monthly_sales.png",
    dpi=300
)
plt.close()

# 9. Save summary tables
customer_summary.to_csv(
    OUTPUT_DIR / "step3_customer_summary.csv",
    index=False
)

category_sales.rename("Total_Sales").to_csv(
    OUTPUT_DIR / "step3_category_sales.csv"
)

monthly_sales.rename("Total_Sales").to_csv(
    OUTPUT_DIR / "step3_monthly_sales.csv"
)

# 10. Final checks
print("\n=== PRODUCT CATEGORY SALES ===")
print(category_sales)

print("\n=== MONTHLY SALES ===")
print(monthly_sales)

print("\n=== OUTPUT CHECK ===")
print("Customer records:", len(customer_summary))
print("Total orders:", df["Order_ID"].nunique())
print(
    "Spending totals match:",
    abs(
        customer_summary["Total_Spending"].sum()
        - df["Total_Amount"].sum()
    ) < 0.01
)
print(
    "Order counts match:",
    customer_summary["Purchase_Frequency"].sum()
    == df["Order_ID"].nunique()
)

print("\nStep 3 completed successfully!")
