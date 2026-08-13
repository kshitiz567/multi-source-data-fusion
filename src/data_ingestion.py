import pandas as pd
import json
import os

print("=" * 60)
print("MULTI-SOURCE DATA INGESTION")
print("=" * 60)

# --------------------------------------------------
# 1. Load CSV - Sales
# --------------------------------------------------

sales_path = "data/raw/sales.csv"

sales_df = pd.read_csv(sales_path)

print("\n✓ Sales CSV loaded")
print("  Rows:", sales_df.shape[0])
print("  Columns:", sales_df.shape[1])


# --------------------------------------------------
# 2. Load Excel - Customers
# --------------------------------------------------

customers_path = "data/raw/customers.xlsx"

customers_df = pd.read_excel(customers_path)

print("\n✓ Customer Excel loaded")
print("  Rows:", customers_df.shape[0])
print("  Columns:", customers_df.shape[1])


# --------------------------------------------------
# 3. Load JSON - Products
# --------------------------------------------------

products_path = "data/raw/products.json"

with open(products_path, "r", encoding="utf-8") as file:
    products_data = json.load(file)

products_df = pd.DataFrame(products_data)

print("\n✓ Products JSON loaded")
print("  Rows:", products_df.shape[0])
print("  Columns:", products_df.shape[1])


# --------------------------------------------------
# 4. Load External CSV
# --------------------------------------------------

market_path = "data/external/market_data.csv"

market_df = pd.read_csv(market_path)

print("\n✓ External market data loaded")
print("  Rows:", market_df.shape[0])
print("  Columns:", market_df.shape[1])


# --------------------------------------------------
# 5. Display column information
# --------------------------------------------------

print("\n" + "=" * 60)
print("SOURCE COLUMN STRUCTURE")
print("=" * 60)

print("\nSALES:")
print(list(sales_df.columns))

print("\nCUSTOMERS:")
print(list(customers_df.columns))

print("\nPRODUCTS:")
print(list(products_df.columns))

print("\nMARKET DATA:")
print(list(market_df.columns))


# --------------------------------------------------
# 6. Display sample records
# --------------------------------------------------

print("\n" + "=" * 60)
print("SAMPLE RECORDS")
print("=" * 60)

print("\nSales:")
print(sales_df.head(3))

print("\nCustomers:")
print(customers_df.head(3))

print("\nProducts:")
print(products_df.head(3))

print("\nMarket Data:")
print(market_df.head(3))


print("\n" + "=" * 60)
print("DATA INGESTION COMPLETED SUCCESSFULLY")
print("=" * 60)