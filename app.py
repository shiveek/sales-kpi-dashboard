import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# PAGE CONFIG
# --------------------------
st.set_page_config(
    page_title="Sales KPI Dashboard",
    layout="wide"
)

st.title("📊 Sales KPI Dashboard")

# --------------------------
# LOAD DATA
# --------------------------
try:
    df = pd.read_csv("sales_data.csv")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Display columns for debugging
st.write("Columns found in CSV:", df.columns.tolist())

# --------------------------
# CHECK REQUIRED COLUMNS
# --------------------------
required_columns = [
    "Order Date",
    "Region",
    "Category",
    "Sales",
    "Profit",
    "Order ID",
    "Product Name"
]

missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns: {missing_cols}")
    st.stop()

# --------------------------
# DATE CONVERSION
# --------------------------
df["Order Date"] = pd.to_datetime(
    df["Order Date"],
    errors="coerce"
)

df = df.dropna(subset=["Order Date"])

# --------------------------
# SIDEBAR FILTERS
# --------------------------
st.sidebar.header("Filters")

selected_regions = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

filtered_df = df[
    (df["Region"].isin(selected_regions)) &
    (df["Category"].isin(selected_categories))
]

# --------------------------
# KPIs
# --------------------------
total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()

avg_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

# --------------------------
# KPI CARDS
# --------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.2f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.2f}"
)

col3.metric(
    "Total Orders",
    total_orders
)

col4.metric(
    "Average Order Value",
    f"${avg_order_value:,.2f}"
)

st.markdown("---")

# --------------------------
# MONTHLY SALES TREND
# --------------------------
monthly_sales = (
    filtered_df
    .groupby(
        filtered_df["Order Date"].dt.to_period("M")
    )["Sales"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = monthly_sales["Order Date"].astype(str)

fig1 = px.line(
    monthly_sales,
    x="Order Date",
    y="Sales",
    title="Monthly Sales Trend"
)

st.plotly_chart(fig1, use_container_width=True)

# --------------------------
# SALES BY CATEGORY
# --------------------------
category_sales = (
    filtered_df
    .groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.bar(
    category_sales,
    x="Category",
    y="Sales",
    title="Sales by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# --------------------------
# PROFIT BY REGION
# --------------------------
region_profit = (
    filtered_df
    .groupby("Region")["Profit"]
    .sum()
    .reset_index()
)

fig3 = px.pie(
    region_profit,
    names="Region",
    values="Profit",
    title="Profit by Region"
)

st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# TOP PRODUCTS
# --------------------------
top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig4 = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales"
)

st.plotly_chart(fig4, use_container_width=True)

# --------------------------
# SALES VS PROFIT
# --------------------------
fig5 = px.scatter(
    filtered_df,
    x="Sales",
    y="Profit",
    color="Category",
    title="Sales vs Profit"
)

st.plotly_chart(fig5, use_container_width=True)

st.success("✅ Dashboard Loaded Successfully")