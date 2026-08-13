import os
import random
import json
import pandas as pd
import numpy as np

# Reproducibility
random.seed(42)
np.random.seed(42)

# --------------------------------------------------
# Create folders
# --------------------------------------------------

os.makedirs("data/raw", exist_ok=True)
os.makedirs("data/external", exist_ok=True)
os.makedirs("data/processed", exist_ok=True)

# --------------------------------------------------
# CUSTOMER DATA
# --------------------------------------------------

customers = [
    ("C001", "Rahul Sharma", "Delhi", "North"),
    ("C002", "Priya Mehta", "Mumbai", "West"),
    ("C003", "Aman Verma", "Bengaluru", "South"),
    ("C004", "Sneha Kapoor", "New Delhi", "North"),
    ("C005", "Arjun Singh", "Pune", "West"),
    ("C006", "Neha Gupta", "Hyderabad", "South"),
    ("C007", "Rohit Kumar", "Delhi", "North"),
    ("C008", "Ananya Iyer", "Chennai", "South"),
    ("C009", "Vikram Patel", "Ahmedabad", "West"),
    ("C010", "Kavya Nair", "Kochi", "South"),
    ("C011", "Aditya Joshi", "Jaipur", "North"),
    ("C012", "Meera Shah", "Mumbai", "West"),
    ("C013", "Karan Malhotra", "Gurugram", "North"),
    ("C014", "Pooja Rao", "Hyderabad", "South"),
    ("C015", "Sahil Jain", "Bengaluru", "South"),
]

customers_df = pd.DataFrame(
    customers,
    columns=["customer_id", "customer_name", "city", "region"]
)

# Add intentional formatting inconsistencies
customers_df.loc[1, "city"] = "mumbai"
customers_df.loc[3, "customer_name"] = "Sneha  Kapoor"
customers_df.loc[6, "city"] = "Delhi "
customers_df.loc[9, "customer_name"] = "Kavya Nair "

customers_df.to_excel(
    "data/raw/customers.xlsx",
    index=False
)

# --------------------------------------------------
# PRODUCT DATA
# --------------------------------------------------

products = [
    ("P001", "Laptop Pro", "Electronics", "TechNova", 65000),
    ("P002", "Wireless Headphones", "Electronics", "SoundMax", 4500),
    ("P003", "Smart Watch", "Electronics", "FitTech", 7000),
    ("P004", "Running Shoes", "Sports", "Sportify", 3500),
    ("P005", "Office Chair", "Furniture", "ComfortCo", 9000),
    ("P006", "Backpack", "Accessories", "UrbanGear", 2200),
    ("P007", "Coffee Maker", "Home Appliances", "BrewMaster", 5500),
    ("P008", "Smartphone X", "Electronics", "TechNova", 32000),
    ("P009", "Yoga Mat", "Sports", "FitLife", 1500),
    ("P010", "Desk Lamp", "Furniture", "BrightHome", 1800),
]

products_json = [
    {
        "product_id": p[0],
        "product_name": p[1],
        "category": p[2],
        "brand": p[3],
        "price": p[4]
    }
    for p in products
]

with open("data/raw/products.json", "w", encoding="utf-8") as f:
    json.dump(products_json, f, indent=4)

# --------------------------------------------------
# SALES DATA
# --------------------------------------------------

sales_rows = []

for i in range(1, 501):

    customer = random.choice(customers)
    product = random.choice(products)

    quantity = random.randint(1, 5)
    price = product[4]

    revenue = quantity * price

    date = pd.Timestamp("2024-01-01") + pd.Timedelta(
        days=random.randint(0, 364)
    )

    sales_rows.append(
        {
            "order_id": f"O{i:04d}",
            "customer": customer[1],
            "cust_id": customer[0],
            "product": product[1],
            "product_id": product[0],
            "quantity": quantity,
            "revenue": revenue,
            "order_date": date.strftime("%Y-%m-%d"),
        }
    )

sales_df = pd.DataFrame(sales_rows)

# Intentional inconsistencies
sales_df.loc[10, "customer"] = "Rahul  Sharma"
sales_df.loc[20, "customer"] = "R. Sharma"
sales_df.loc[30, "customer"] = "Priya Mehta "
sales_df.loc[40, "customer"] = "Aman  Verma"

# Different date formats
sales_df.loc[50, "order_date"] = "15/02/2024"
sales_df.loc[51, "order_date"] = "03-18-2024"

# Missing values
sales_df.loc[60, "customer"] = np.nan
sales_df.loc[61, "product"] = np.nan

# Duplicate rows
sales_df = pd.concat(
    [sales_df, sales_df.iloc[[100, 200, 300]]],
    ignore_index=True
)

sales_df.to_csv(
    "data/raw/sales.csv",
    index=False
)

# --------------------------------------------------
# EXTERNAL MARKET DATA
# --------------------------------------------------

dates = pd.date_range(
    start="2024-01-01",
    end="2024-12-31",
    freq="MS"
)

market_data = pd.DataFrame(
    {
        "month": dates,
        "market_index": np.random.uniform(
            18000, 24000, len(dates)
        ).round(2),
        "consumer_confidence": np.random.uniform(
            70, 100, len(dates)
        ).round(2),
        "inflation_rate": np.random.uniform(
            4, 7, len(dates)
        ).round(2),
    }
)

market_data["month"] = market_data["month"].dt.strftime(
    "%Y-%m-%d"
)

market_data.to_csv(
    "data/external/market_data.csv",
    index=False
)

print("==========================================")
print("DATA GENERATION COMPLETED SUCCESSFULLY")
print("==========================================")

print("\nFiles created:")

print("✓ data/raw/customers.xlsx")
print("✓ data/raw/products.json")
print("✓ data/raw/sales.csv")
print("✓ data/external/market_data.csv")

print("\nSales records:", len(sales_df))
print("Customer records:", len(customers_df))
print("Product records:", len(products_df) if "products_df" in locals() else len(products))
print("Market records:", len(market_data))