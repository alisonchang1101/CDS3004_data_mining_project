
import pandas as pd
from pathlib import Path

# 1. Load dataset
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ecommerce_customer_behavior_dataset_v2.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

# 2. Dataset structure
print("=== 1. DATASET SHAPE ===")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n=== 2. FIRST 5 ROWS ===")
print(df.head().to_string())

print("\n=== 3. COLUMN INFORMATION ===")
df.info()

# 3. Data quality overview
print("\n=== 4. MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== 5. DUPLICATE ROWS ===")
print(df.duplicated().sum())

# 4. Customer and transaction information
print("\n=== 6. UNIQUE CUSTOMERS ===")
print(df["Customer_ID"].nunique())

print("\n=== 7. UNIQUE ORDERS ===")
print(df["Order_ID"].nunique())

print("\n=== 8. DATE RANGE ===")
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
print("Start:", df["Date"].min())
print("End:", df["Date"].max())
print("Invalid dates:", df["Date"].isna().sum())

# 5. Purchase behavior overview
print("\n=== 9. PURCHASE BEHAVIOR ===")
print(df[["Quantity", "Unit_Price", "Discount_Amount",
          "Total_Amount"]].describe())

# 6. Customer purchase frequency
customer_orders = df.groupby("Customer_ID")["Order_ID"].nunique()

print("\n=== 10. ORDERS PER CUSTOMER ===")
print(customer_orders.describe())
print("Customers with 2+ orders:", (customer_orders >= 2).sum())

# 7. Product categories
print("\n=== 11. PRODUCT CATEGORIES ===")
print(df["Product_Category"].value_counts())

# 8. Save results
summary = pd.DataFrame({
    "Metric": [
        "Total Records",
        "Total Columns",
        "Unique Customers",
        "Unique Orders",
        "Duplicate Rows",
        "Customers with 2+ Orders",
        "Invalid Dates"
    ],
    "Value": [
        len(df),
        len(df.columns),
        df["Customer_ID"].nunique(),
        df["Order_ID"].nunique(),
        df.duplicated().sum(),
        (customer_orders >= 2).sum(),
        df["Date"].isna().sum()
    ]
})

summary.to_csv(
    OUTPUT_DIR / "step1_summary.csv",
    index=False
)

print("\nStep 1 completed successfully!")
