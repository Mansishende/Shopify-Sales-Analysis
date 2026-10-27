
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="Shopify | Sales Intelligence",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "shopify_cleaned.csv"

# --------------------------------------------------
# PREMIUM DARK THEME
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #0B1120;
    color: #E5EDF7;
}

[data-testid="stHeader"] {
    background: rgba(11, 17, 32, 0.9);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

[data-testid="stSidebar"] {
    background: #101A2B;
    border-right: 1px solid #24344B;
}

[data-testid="stMetric"] {
    background: linear-gradient(145deg, #17253A, #111C2D);
    border: 1px solid #2B3D55;
    border-radius: 16px;
    padding: 20px 18px;
    min-height: 125px;
}

[data-testid="stMetricLabel"] {
    color: #9BAEC6;
    font-size: 0.9rem;
}

[data-testid="stMetricValue"] {
    color: #F1F5F9;
    font-weight: 800;
}

h1, h2, h3 {
    color: #F1F5F9 !important;
    letter-spacing: -0.5px;
}

p, label {
    color: #B6C5D8;
}

div[data-testid="stVerticalBlockBorderWrapper"] {
    border-color: #263750;
    border-radius: 16px;
}

.stButton > button {
    background: #14B8A6;
    color: #07131D;
    font-weight: 700;
    border: none;
    border-radius: 10px;
    min-height: 42px;
}

.stButton > button:hover {
    background: #5EEAD4;
    color: #07131D;
}

hr {
    border-color: #263750;
}

.small-caption {
    color: #8EA2BB;
    font-size: 0.85rem;
}

.hero {
    background: linear-gradient(115deg, #14243A, #123A43);
    border: 1px solid #28505B;
    border-radius: 20px;
    padding: 28px 30px;
    margin-bottom: 24px;
}

.hero-tag {
    color: #5EEAD4;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 2px;
}

.hero-title {
    color: #F8FAFC;
    font-size: 2.1rem;
    font-weight: 800;
    margin: 8px 0;
}

.hero-subtitle {
    color: #B6C8D9;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data(file_path, modified_time):
    return pd.read_csv(file_path)

# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def find_column(columns, keywords):
    """Find a column using common name variations."""
    for keyword in keywords:
        for col in columns:
            if keyword in col.lower():
                return col
    return None


def money(value):
    return f"${value:,.2f}"


def make_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#C6D4E5", family="Inter"),
        margin=dict(l=15, r=15, t=45, b=15),
        title_font=dict(size=16, color="#F1F5F9"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(
        gridcolor="#263750",
        zeroline=False,
        title=None
    )
    return fig


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🛍️ SHOPIFY")
    st.caption("SALES INTELLIGENCE")
    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Executive Overview", "Sales Explorer", "Data Table"],
    )

    st.divider()
    st.markdown("### About this dashboard")
    st.caption(
        "A sales analytics workspace for exploring "
        "revenue, orders, customers, and product performance."
    )
    st.caption("Built with Python · Pandas · Streamlit · Plotly")

# --------------------------------------------------
# CHECK DATA FILE
# --------------------------------------------------
if not DATA_FILE.exists():
    st.error(
        "The cleaned dataset was not found at "
        "`data/shopify_cleaned.csv`."
    )
    st.info(
        "Check that app.py is in the main project folder "
        "and shopify_cleaned.csv is inside the data folder."
    )
    st.stop()

try:
    df = load_data(str(DATA_FILE), DATA_FILE.stat().st_mtime)
except Exception as error:
    st.error(f"Could not read the sales dataset: {error}")
    st.stop()

if df.empty:
    st.warning("Your dataset is empty. Please check the CSV file.")
    st.stop()

df.columns = df.columns.str.strip()
columns = list(df.columns)

# Identify likely columns
revenue_col = find_column(
    columns,
    ["total price usd", "total revenue", "revenue", "sales amount"]
)
order_col = find_column(
    columns,
    ["order number", "order id", "order_id", "order"]
)
customer_col = find_column(
    columns,
    ["customer id", "customer_id", "customer"]
)
quantity_col = find_column(
    columns,
    ["quantity", "qty"]
)
date_col = find_column(
    columns,
    ["created at", "order date", "order_date", "date", "created"]
)
product_col = find_column(
    columns,
    ["product title", "product name", "product"]
)

# Convert numeric columns safely
if revenue_col:
    df[revenue_col] = pd.to_numeric(
        df[revenue_col].astype(str).str.replace(",", "", regex=False),
        errors="coerce"
    )

if quantity_col:
    df[quantity_col] = pd.to_numeric(
        df[quantity_col], errors="coerce"
    )

# --------------------------------------------------
# HERO HEADER
# --------------------------------------------------
st.markdown("""
<div class="hero">
    <div class="hero-tag">BUSINESS PERFORMANCE CENTER</div>
    <div class="hero-title">Sales Intelligence Dashboard</div>
    <div class="hero-subtitle">
        Understand your sales performance, discover product trends,
        and explore your Shopify data in one place.
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# FILTERS
# --------------------------------------------------
with st.expander("⚙️ Customize your dashboard filters", expanded=False):
    filter_options = {}

    possible_filters = [
        c for c in columns
        if any(word in c.lower() for word in [
            "country", "province", "city", "region", "category"
        ])
    ]

    filter_cols = st.columns(min(max(len(possible_filters), 1), 3))

    for i, col in enumerate(possible_filters):
        with filter_cols[i % len(filter_cols)]:
            values = sorted(
                df[col].dropna().astype(str).unique().tolist()
            )
            selected = st.multiselect(
                f"Filter: {col}",
                options=values,
                key=f"filter_{col}",
            )
            if selected:
                filter_options[col] = selected

filtered = df.copy()

for col, selected in filter_options.items():
    filtered = filtered[filtered[col].astype(str).isin(selected)]

if filtered.empty:
    st.warning("No rows match these filters. Clear a filter to see your data.")
    st.stop()

# --------------------------------------------------
# CALCULATE KPIs
# --------------------------------------------------
revenue = (
    filtered[revenue_col].fillna(0).sum()
    if revenue_col else 0
)

orders = (
    filtered[order_col].nunique()
    if order_col else len(filtered)
)

customers = (
    filtered[customer_col].nunique()
    if customer_col else None
)

aov = revenue / orders if orders else 0

st.markdown("### Executive snapshot")
st.caption("Key performance indicators for the selected data")

k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Revenue", money(revenue))
k2.metric("Total Orders", f"{orders:,}")
k3.metric(
    "Unique Customers",
    f"{customers:,}" if customers is not None else "N/A"
)
k4.metric("Average Order Value", money(aov))

if quantity_col:
    total_quantity = filtered[quantity_col].fillna(0).sum()
    st.caption(f"📦 Total quantity sold: {total_quantity:,.0f}")

# --------------------------------------------------
# EXECUTIVE OVERVIEW
# --------------------------------------------------
if page == "Executive Overview":
    left, right = st.columns([1.55, 1])

    with left:
        with st.container(border=True):
            st.markdown("#### 📈 Revenue trend")

            if date_col and revenue_col:
                dates = pd.to_datetime(
                    filtered[date_col], errors="coerce"
                )
                trend_data = filtered.copy()
                trend_data["_date"] = dates
                trend_data = trend_data.dropna(subset=["_date"])

                if not trend_data.empty:
                    trend_data["_month"] = (
                        trend_data["_date"].dt.to_period("M").astype(str)
                    )
                    monthly = (
                        trend_data.groupby("_month", as_index=False)[revenue_col]
                        .sum()
                        .sort_values("_month")
                    )

                    fig = px.line(
                        monthly,
                        x="_month",
                        y=revenue_col,
                        markers=True,
                        labels={
                            "_month": "Month",
                            revenue_col: "Revenue (USD)"
                        },
                    )
                    fig.update_traces(
                        line=dict(color="#2DD4BF", width=3),
                        marker=dict(size=7, color="#5EEAD4"),
                        fill="tozeroy",
                        fillcolor="rgba(45,212,191,0.10)",
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No usable dates were found in the date column.")
            else:
                st.info(
                    "A date column and a revenue column are needed "
                    "to show the revenue trend."
                )

    with right:
        with st.container(border=True):
            st.markdown("#### 🏆 Top products")

            if product_col and revenue_col:
                products = (
                    filtered.groupby(product_col)[revenue_col]
                    .sum()
                    .nlargest(10)
                    .sort_values()
                    .reset_index()
                )

                fig = px.bar(
                    products,
                    x=revenue_col,
                    y=product_col,
                    orientation="h",
                    labels={
                        revenue_col: "Revenue (USD)",
                        product_col: "Product"
                    },
                )
                fig.update_traces(
                    marker_color="#38BDF8",
                    marker_line_width=0,
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(
                    "A product-name column and revenue column are needed "
                    "for this chart."
                )

    with st.container(border=True):
        st.markdown("#### 📊 Revenue distribution")

        if product_col and revenue_col:
            category_sales = (
                filtered.groupby(product_col)[revenue_col]
                .sum()
                .nlargest(6)
                .reset_index()
            )

            if not category_sales.empty:
                fig = px.pie(
                    category_sales,
                    names=product_col,
                    values=revenue_col,
                    hole=0.62,
                )
                fig.update_traces(
                    textposition="inside",
                    textinfo="percent",
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Product and revenue fields are required for this chart.")

# --------------------------------------------------
# SALES EXPLORER
# --------------------------------------------------
elif page == "Sales Explorer":
    st.markdown("### Explore sales performance")
    st.caption("Compare products and inspect the available sales fields.")

    if product_col and revenue_col:
        product_sales = (
            filtered.groupby(product_col, as_index=False)[revenue_col]
            .sum()
            .sort_values(revenue_col, ascending=False)
        )
        st.dataframe(
            product_sales,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info("Product-level analysis needs product and revenue columns.")

    if date_col and revenue_col:
        dates = pd.to_datetime(filtered[date_col], errors="coerce")
        timed = filtered.copy()
        timed["_date"] = dates
        timed = timed.dropna(subset=["_date"])

        if not timed.empty:
            timed["_month"] = timed["_date"].dt.to_period("M").astype(str)
            monthly = (
                timed.groupby("_month", as_index=False)[revenue_col]
                .sum()
                .sort_values("_month")
            )

            fig = px.bar(
                monthly,
                x="_month",
                y=revenue_col,
                labels={"_month": "Month", revenue_col: "Revenue (USD)"},
            )
            fig.update_traces(marker_color="#2DD4BF")
            st.plotly_chart(make_chart(fig), use_container_width=True)

# --------------------------------------------------
# DATA TABLE
# --------------------------------------------------
elif page == "Data Table":
    st.markdown("### Sales data explorer")
    st.caption("Search and review the filtered records from your dataset.")

    search_text = st.text_input(
        "🔎 Search across text fields",
        placeholder="Type a product, country, customer, or other value...",
    )

    table_data = filtered.copy()

    if search_text:
        text_cols = table_data.select_dtypes(
            include=["object", "string"]
        ).columns

        if len(text_cols):
            mask = table_data[text_cols].astype(str).apply(
                lambda col: col.str.contains(
                    search_text, case=False, na=False
                )
            ).any(axis=1)
            table_data = table_data[mask]

    st.caption(f"{len(table_data):,} records found")
    st.dataframe(
        table_data,
        use_container_width=True,
        hide_index=True,
        height=500,
    )

    st.download_button(
        "⬇️ Download filtered data as CSV",
        data=table_data.to_csv(index=False).encode("utf-8"),
        file_name="shopify_filtered_sales.csv",
        mime="text/csv",
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()
st.markdown(
    '<p class="small-caption">SHOPIFY SALES INTELLIGENCE · '
    'Built with Python, Pandas, Streamlit & Plotly</p>',
    unsafe_allow_html=True,
)
