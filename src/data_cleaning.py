import pandas as pd
import json

print("=" * 60)
print("DATA QUALITY & STANDARDIZATION")
print("=" * 60)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

sales_df = pd.read_csv("data/raw/sales.csv")
customers_df = pd.read_excel("data/raw/customers.xlsx")

with open("data/raw/products.json", "r", encoding="utf-8") as file:
    products_df = pd.DataFrame(json.load(file))

market_df = pd.read_csv("data/external/market_data.csv")


# --------------------------------------------------
# 1. INSPECT MISSING VALUES
# --------------------------------------------------

print("\n" + "=" * 60)
print("MISSING VALUES BEFORE CLEANING")
print("=" * 60)

print("\nSales:")
print(sales_df.isnull().sum())

print("\nCustomers:")
print(customers_df.isnull().sum())

print("\nProducts:")
print(products_df.isnull().sum())

print("\nMarket Data:")
print(market_df.isnull().sum())


# --------------------------------------------------
# 2. REMOVE DUPLICATE SALES
# --------------------------------------------------

sales_before = len(sales_df)

sales_df = sales_df.drop_duplicates()

sales_after = len(sales_df)

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

print("Sales records before:", sales_before)
print("Sales records after :", sales_after)
print("Duplicates removed  :", sales_before - sales_after)


# --------------------------------------------------
# 3. STANDARDIZE CUSTOMER NAMES
# --------------------------------------------------

customers_df["customer_name"] = (
    customers_df["customer_name"]
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)

sales_df["customer"] = (
    sales_df["customer"]
    .fillna("Unknown")
    .astype(str)
    .str.strip()
    .str.replace(r"\s+", " ", regex=True)
)


# --------------------------------------------------
# 4. STANDARDIZE CITY NAMES
# --------------------------------------------------

def standardize_city(city):

    if pd.isna(city):
        return "Unknown"

    city = str(city).strip().lower()

    city_mapping = {
        "delhi": "Delhi",
        "new delhi": "Delhi",
        "mumbai": "Mumbai",
        "bengaluru": "Bengaluru",
        "bangalore": "Bengaluru",
        "gurugram": "Gurugram",
        "gurgaon": "Gurugram",
        "hyderabad": "Hyderabad",
        "chennai": "Chennai",
        "pune": "Pune",
        "jaipur": "Jaipur",
        "ahmedabad": "Ahmedabad",
        "kochi": "Kochi"
    }

    return city_mapping.get(city, city.title())


customers_df["city"] = customers_df["city"].apply(
    standardize_city
)


# --------------------------------------------------
# 5. STANDARDIZE DATE FORMAT
# --------------------------------------------------

sales_df["order_date"] = pd.to_datetime(
    sales_df["order_date"],
    errors="coerce",
    dayfirst=True
)

market_df["month"] = pd.to_datetime(
    market_df["month"],
    errors="coerce"
)


# --------------------------------------------------
# 6. HANDLE MISSING VALUES
# --------------------------------------------------

sales_df["customer"] = sales_df["customer"].replace(
    ["nan", "None", ""],
    "Unknown"
)

sales_df["product"] = sales_df["product"].fillna(
    "Unknown Product"
)

customers_df["city"] = customers_df["city"].fillna(
    "Unknown"
)


# --------------------------------------------------
# 7. STANDARDIZE COLUMN NAMES
# --------------------------------------------------

sales_df.columns = (
    sales_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

customers_df.columns = (
    customers_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

products_df.columns = (
    products_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

market_df.columns = (
    market_df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# --------------------------------------------------
# 8. SAVE CLEAN DATA
# --------------------------------------------------

sales_df.to_csv(
    "data/processed/clean_sales.csv",
    index=False
)

customers_df.to_csv(
    "data/processed/clean_customers.csv",
    index=False
)

products_df.to_csv(
    "data/processed/clean_products.csv",
    index=False
)

market_df.to_csv(
    "data/processed/clean_market_data.csv",
    index=False
)


# --------------------------------------------------
# 9. FINAL QUALITY REPORT
# --------------------------------------------------

print("\n" + "=" * 60)
print("DATA QUALITY AFTER CLEANING")
print("=" * 60)

print("\nSales missing values:")
print(sales_df.isnull().sum())

print("\nCustomer missing values:")
print(customers_df.isnull().sum())

print("\nProduct missing values:")
print(products_df.isnull().sum())

print("\nMarket missing values:")
print(market_df.isnull().sum())


print("\n" + "=" * 60)
print("CLEANING COMPLETED SUCCESSFULLY")
print("=" * 60)

print("\nClean files created:")
print("✓ data/processed/clean_sales.csv")
print("✓ data/processed/clean_customers.csv")
print("✓ data/processed/clean_products.csv")
print("✓ data/processed/clean_market_data.csv")