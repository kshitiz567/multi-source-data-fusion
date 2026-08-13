import pandas as pd
from rapidfuzz import process, fuzz

print("=" * 65)
print("ENTITY RESOLUTION & FUZZY MATCHING")
print("=" * 65)


# --------------------------------------------------
# 1. LOAD CLEAN DATA
# --------------------------------------------------

sales_df = pd.read_csv(
    "data/processed/clean_sales.csv"
)

customers_df = pd.read_csv(
    "data/processed/clean_customers.csv"
)


# --------------------------------------------------
# 2. CREATE NORMALIZED NAMES
# --------------------------------------------------

def normalize_name(name):

    if pd.isna(name):
        return ""

    name = str(name).lower().strip()

    name = name.replace(".", "")

    name = " ".join(name.split())

    return name


sales_df["normalized_customer"] = (
    sales_df["customer"]
    .apply(normalize_name)
)

customers_df["normalized_name"] = (
    customers_df["customer_name"]
    .apply(normalize_name)
)


# --------------------------------------------------
# 3. CUSTOMER MASTER LIST
# --------------------------------------------------

customer_master = (
    customers_df["normalized_name"]
    .dropna()
    .unique()
    .tolist()
)


# --------------------------------------------------
# 4. FUZZY MATCHING FUNCTION
# --------------------------------------------------

def find_best_match(name):

    if not name or name == "unknown":

        return pd.Series(
            ["Unknown", "Unknown", 0]
        )

    # Special abbreviation handling
    aliases = {
        "r sharma": "rahul sharma",
        "p mehta": "priya mehta",
        "a verma": "aman verma"
    }

    if name in aliases:

        matched_name = aliases[name]

        return pd.Series(
            [matched_name, "Alias Match", 100]
        )

    result = process.extractOne(
        name,
        customer_master,
        scorer=fuzz.token_sort_ratio
    )

    if result is None:

        return pd.Series(
            ["Unknown", "No Match", 0]
        )

    matched_name = result[0]
    score = result[1]

    if score >= 85:

        status = "High Confidence"

    elif score >= 70:

        status = "Medium Confidence"

    else:

        status = "Low Confidence"

    return pd.Series(
        [matched_name, status, round(score, 2)]
    )


# --------------------------------------------------
# 5. APPLY ENTITY RESOLUTION
# --------------------------------------------------

sales_df[
    [
        "matched_customer",
        "match_status",
        "match_score"
    ]
] = sales_df[
    "normalized_customer"
].apply(find_best_match)


# --------------------------------------------------
# 6. CONNECT TO CUSTOMER ID
# --------------------------------------------------

customer_lookup = customers_df[
    [
        "customer_id",
        "normalized_name"
    ]
].drop_duplicates()


sales_df = sales_df.merge(
    customer_lookup,
    left_on="matched_customer",
    right_on="normalized_name",
    how="left"
)


# --------------------------------------------------
# 7. DISPLAY MATCHING RESULTS
# --------------------------------------------------

print("\n" + "=" * 65)
print("ENTITY MATCHING RESULTS")
print("=" * 65)

display_columns = [
    "customer",
    "matched_customer",
    "customer_id",
    "match_status",
    "match_score"
]

print(
    sales_df[
        display_columns
    ].head(20).to_string(index=False)
)


# --------------------------------------------------
# 8. MATCH QUALITY SUMMARY
# --------------------------------------------------

print("\n" + "=" * 65)
print("MATCH QUALITY SUMMARY")
print("=" * 65)

print(
    sales_df["match_status"]
    .value_counts()
)


# --------------------------------------------------
# 9. LOW-CONFIDENCE MATCHES
# --------------------------------------------------

low_confidence = sales_df[
    sales_df["match_status"]
    == "Low Confidence"
]

print("\nLow-confidence matches:")

if len(low_confidence) == 0:

    print("None")

else:

    print(
        low_confidence[
            [
                "customer",
                "matched_customer",
                "match_score"
            ]
        ].head(20).to_string(index=False)
    )


# --------------------------------------------------
# 10. SAVE RESOLVED DATA
# --------------------------------------------------

sales_df.to_csv(
    "data/processed/resolved_sales.csv",
    index=False
)


print("\n" + "=" * 65)
print("ENTITY RESOLUTION COMPLETED SUCCESSFULLY")
print("=" * 65)

print(
    "\n✓ data/processed/resolved_sales.csv created"
)