
import pandas as pd
from pathlib import Path

# 1. Load original data
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "ecommerce_customer_behavior_dataset_v2.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(DATA_PATH)

print("=== ORIGINAL DATA ===")
print("Rows:", len(df))
print("Columns:", len(df.columns))

# 2. Check missing values
print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

# 3. Check duplicate records
print("\n=== DUPLICATE ROWS ===")
print(df.duplicated().sum())

# 4. Check invalid numerical values
print("\n=== INVALID NUMERICAL VALUES ===")

for col in ["Quantity", "Unit_Price",
            "Discount_Amount", "Total_Amount"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

print("Quantity <= 0:", (df["Quantity"] <= 0).sum())
print("Unit_Price < 0:", (df["Unit_Price"] < 0).sum())
print("Discount_Amount < 0:",
      (df["Discount_Amount"] < 0).sum())
print("Total_Amount < 0:",
      (df["Total_Amount"] < 0).sum())

# 5. Check date format
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

print("\n=== INVALID DATES ===")
print(df["Date"].isna().sum())

# 6. Check amount consistency
expected_amount = (
    df["Quantity"] * df["Unit_Price"]
    - df["Discount_Amount"]
)

difference = abs(df["Total_Amount"] - expected_amount)

print("\n=== AMOUNT CONSISTENCY ===")
print("Inconsistent amounts:",
      (difference > 0.01).sum())

# 7. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates().copy()

print("\n=== CLEANING SUMMARY ===")
print("Original rows:", before)
print("Rows after removing exact duplicates:", len(df))
print("Removed duplicates:", before - len(df))

# 8. Save preliminary cleaned data
df.to_csv(
    OUTPUT_DIR / "step2_preliminary_cleaned.csv",
    index=False
)

print("\nStep 2 completed successfully!")
