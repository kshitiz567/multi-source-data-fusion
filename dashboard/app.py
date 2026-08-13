import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="NexaMart | Data Fusion Intelligence",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/processed/fused_dataset.csv"
    )

    df["order_date"] = pd.to_datetime(
        df["order_date"],
        errors="coerce"
    )

    return df


df = load_data()


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 NexaMart Data Fusion Intelligence Platform")

st.markdown(
    """
    **Multi-Source Business Intelligence Dashboard**

    This dashboard combines sales, customer, product,
    and external market data into a unified analytical view.
    """
)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Filters")

# Category filter
categories = sorted(
    df["category"]
    .dropna()
    .unique()
    .tolist()
)

selected_categories = st.sidebar.multiselect(
    "Product Category",
    categories,
    default=categories
)

# City filter
cities = sorted(
    df["city"]
    .dropna()
    .unique()
    .tolist()
)

selected_cities = st.sidebar.multiselect(
    "City",
    cities,
    default=cities
)


# Apply filters
filtered_df = df[
    df["category"].isin(selected_categories)
    & df["city"].isin(selected_cities)
]


# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_revenue = filtered_df["revenue"].sum()

total_orders = filtered_df["order_id"].nunique()

total_customers = filtered_df["customer_id"].nunique()

total_products = filtered_df["product_id"].nunique()

average_order_value = (
    total_revenue / total_orders
    if total_orders > 0
    else 0
)


# --------------------------------------------------
# KPI CARDS
# --------------------------------------------------
st.info(
    """
    🔗 **Data Fusion Pipeline**

    Customer Data + Product Data + Sales Data + Market Data
    → Entity Resolution → Data Cleaning → Unified Dataset
    """
)

st.subheader("📌 Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

def format_currency(value):
    if value >= 10000000:
        return f"₹{value / 10000000:.2f} Cr"
    elif value >= 100000:
        return f"₹{value / 100000:.2f} L"
    elif value >= 1000:
        return f"₹{value / 1000:.2f} K"
    else:
        return f"₹{value:,.2f}"
    
col1.metric(
    "Total Revenue",
    format_currency(total_revenue)
)

col2.metric(
    "Orders",
    f"{total_orders:,}"
)

col3.metric(
    "Customers",
    f"{total_customers:,}"
)

col4.metric(
    "Products",
    f"{total_products:,}"
)

col5.metric(
    "Avg Order Value",
    f"₹{average_order_value:,.0f}"
)


st.divider()


# --------------------------------------------------
# MONTHLY REVENUE
# --------------------------------------------------

st.subheader("📈 Revenue Trend")

monthly_revenue = (
    filtered_df
    .groupby(
        filtered_df["order_date"].dt.to_period("M")
    )["revenue"]
    .sum()
    .reset_index()
)

monthly_revenue["order_date"] = (
    monthly_revenue["order_date"]
    .astype(str)
)

fig_monthly = px.line(
    monthly_revenue,
    x="order_date",
    y="revenue",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue"
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True
)


# --------------------------------------------------
# CATEGORY + CITY ANALYSIS
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    category_data = (
        filtered_df
        .groupby("category")["revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    fig_category = px.bar(
        category_data,
        x="category",
        y="revenue",
        title="Revenue by Category"
    )

    st.plotly_chart(
        fig_category,
        use_container_width=True
    )


with col2:

    city_data = (
        filtered_df
        .groupby("city")["revenue"]
        .sum()
        .reset_index()
        .sort_values(
            "revenue",
            ascending=False
        )
    )

    fig_city = px.bar(
        city_data,
        x="city",
        y="revenue",
        title="Revenue by City"
    )

    st.plotly_chart(
        fig_city,
        use_container_width=True
    )


# --------------------------------------------------
# TOP PRODUCTS
# --------------------------------------------------

st.subheader("🏆 Top Products")

product_data = (
    filtered_df
    .groupby("product_name")["revenue"]
    .sum()
    .reset_index()
    .sort_values(
        "revenue",
        ascending=False
    )
    .head(10)
)

fig_products = px.bar(
    product_data.sort_values("revenue"),
    x="revenue",
    y="product_name",
    orientation="h",
    title="Top 10 Products by Revenue"
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)


# --------------------------------------------------
# MARKET ANALYSIS
# --------------------------------------------------

st.subheader("🌐 External Market Indicators")

market_data = (
    filtered_df[
        [
            "order_date",
            "revenue",
            "market_index",
            "consumer_confidence",
            "inflation_rate"
        ]
    ]
    .groupby("order_date")
    .agg({
        "revenue": "sum",
        "market_index": "mean",
        "consumer_confidence": "mean",
        "inflation_rate": "mean"
    })
    .reset_index()
)

col1, col2 = st.columns(2)


with col1:

    fig_confidence = px.scatter(
        filtered_df,
        x="consumer_confidence",
        y="revenue",
        title="Consumer Confidence vs Revenue",
        trendline="ols"
    )

    st.plotly_chart(
        fig_confidence,
        use_container_width=True
    )


with col2:

    fig_inflation = px.scatter(
        filtered_df,
        x="inflation_rate",
        y="revenue",
        title="Inflation vs Revenue",
        trendline="ols"
    )

    st.plotly_chart(
        fig_inflation,
        use_container_width=True
    )


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

st.divider()

st.subheader("🔍 Data Quality Overview")

quality_col1, quality_col2, quality_col3 = st.columns(3)

quality_col1.metric(
    "Records",
    f"{len(filtered_df):,}"
)

quality_col2.metric(
    "Missing Values",
    f"{filtered_df.isnull().sum().sum():,}"
)

quality_col3.metric(
    "Duplicate Rows",
    f"{filtered_df.duplicated().sum():,}"
)


# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------

with st.expander("📋 View Unified Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center">

    **NexaMart Data Fusion Intelligence Platform**

    Multi-Source Data Engineering • Entity Resolution • Business Intelligence

    Built with Python • Pandas • Plotly • Streamlit

    </div>
    """,
    unsafe_allow_html=True
)