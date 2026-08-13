import pandas as pd

print("=" * 65)
print("MULTI-SOURCE DATA FUSION")
print("=" * 65)


# --------------------------------------------------
# 1. LOAD RESOLVED SALES
# --------------------------------------------------

sales_df = pd.read_csv(
    "data/processed/resolved_sales.csv"
)

customers_df = pd.read_csv(
    "data/processed/clean_customers.csv"
)

products_df = pd.read_csv(
    "data/processed/clean_products.csv"
)

market_df = pd.read_csv(
    "data/processed/clean_market_data.csv"
)


print("\n✓ All cleaned sources loaded")


# --------------------------------------------------
# 2. PREPARE CUSTOMER DATA
# --------------------------------------------------

customer_lookup = customers_df[
    [
        "customer_id",
        "customer_name",
        "city",
        "region"
    ]
].drop_duplicates(
    subset=["customer_id"]
)


# --------------------------------------------------
# 3. MERGE SALES + CUSTOMERS
# --------------------------------------------------

fused_df = sales_df.merge(
    customer_lookup,
    on="customer_id",
    how="left"
)


print("✓ Sales + Customer data merged")


# --------------------------------------------------
# 4. PREPARE PRODUCT DATA
# --------------------------------------------------

product_lookup = products_df[
    [
        "product_id",
        "product_name",
        "category",
        "brand",
        "price"
    ]
].drop_duplicates(
    subset=["product_id"]
)


# --------------------------------------------------
# 5. MERGE PRODUCTS
# --------------------------------------------------

fused_df = fused_df.merge(
    product_lookup,
    on="product_id",
    how="left"
)


print("✓ Product data merged")


# --------------------------------------------------
# 6. CREATE MONTH COLUMN
# --------------------------------------------------

fused_df["order_date"] = pd.to_datetime(
    fused_df["order_date"],
    errors="coerce"
)

fused_df["month"] = (
    fused_df["order_date"]
    .dt.to_period("M")
    .astype(str)
)


market_df["month"] = pd.to_datetime(
    market_df["month"],
    errors="coerce"
)

market_df["month"] = (
    market_df["month"]
    .dt.to_period("M")
    .astype(str)
)


# --------------------------------------------------
# 7. MERGE EXTERNAL MARKET DATA
# --------------------------------------------------

fused_df = fused_df.merge(
    market_df,
    on="month",
    how="left"
)


print("✓ External market data merged")


# --------------------------------------------------
# 8. REMOVE UNNECESSARY COLUMNS
# --------------------------------------------------

columns_to_remove = [
    "normalized_customer",
    "matched_customer",
    "normalized_name"
]

fused_df = fused_df.drop(
    columns=[
        col for col in columns_to_remove
        if col in fused_df.columns
    ]
)


# --------------------------------------------------
# 9. CALCULATE DERIVED METRICS
# --------------------------------------------------

fused_df["revenue"] = pd.to_numeric(
    fused_df["revenue"],
    errors="coerce"
)

fused_df["quantity"] = pd.to_numeric(
    fused_df["quantity"],
    errors="coerce"
)

fused_df["revenue_per_unit"] = (
    fused_df["revenue"] /
    fused_df["quantity"]
)


# --------------------------------------------------
# 10. DISPLAY FINAL STRUCTURE
# --------------------------------------------------

print("\n" + "=" * 65)
print("FUSED DATASET")
print("=" * 65)

print("Rows:", fused_df.shape[0])
print("Columns:", fused_df.shape[1])

print("\nColumns:")

for column in fused_df.columns:
    print("✓", column)


# --------------------------------------------------
# 11. CHECK DATA QUALITY
# --------------------------------------------------

print("\n" + "=" * 65)
print("FINAL DATA QUALITY CHECK")
print("=" * 65)

print("\nMissing values:")

print(
    fused_df.isnull().sum()
)


# --------------------------------------------------
# 12. SAVE FINAL DATASET
# --------------------------------------------------

fused_df.to_csv(
    "data/processed/fused_dataset.csv",
    index=False
)


print("\n" + "=" * 65)
print("DATA FUSION COMPLETED SUCCESSFULLY")
print("=" * 65)

print(
    "\n✓ data/processed/fused_dataset.csv created"
)