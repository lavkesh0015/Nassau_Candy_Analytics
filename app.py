import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly._subplots import make_subplots

# Dashboard page configuration
st.set_page_config(
    page_title="Nassau Candy Analytics",
    page_icon="🍫",
    layout="wide"
)
# Welcome / Landing Page

if "show_dashboard" not in st.session_state:
    st.session_state.show_dashboard = False

if not st.session_state.show_dashboard:

    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #3b160e, #7b2d26, #c76b36);
    }

    .welcome-box {
        text-align: center;
        padding: 65px 20px 35px 20px;
        color: white;
    }

    .welcome-box h1 {
        font-size: 52px;
        color: #ffe0a3;
    }

    .welcome-box h2 {
        font-size: 27px;
        color: #ffffff;
    }

    .welcome-box p {
        font-size: 18px;
        color: #ffe8d0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="welcome-box">
        <h1>🍫 Welcome to Nassau Candy 🍬</h1>
        <h2>Where Sweetness Meets Smart Analytics!</h2>
        <p>
        Explore product performance, sales trends,
        profitability and business insights.
        </p>
        <h1>🍭 🍬 🍫 🧁 🍩</h1>
        <p>Your journey into Candy Business Analytics starts here.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        if st.button("🍫 Explore Dashboard", use_container_width=True):
            st.session_state.show_dashboard = True
            st.rerun()

    st.stop()
# Dashboard heading
st.title("🍫 Nassau Candy Analytics Dashboard")
st.write("Sales and Profitability Analysis")

# Load dataset
df = pd.read_csv("Data/candy_sales.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
df["Shipping Days"] = (df["Ship Date"]-df["Order Date"]).dt.days
# Factory and Product Mapping

factory_mapping = {
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar - Fudge Mallows": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Lot's O' Nuts",

    "Wonka Bar - Milk Chocolate": "Wicked Choccy's",
    "Wonka Bar - Triple Dazzle Caramel": "Wicked Choccy's",

    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Fun Dip": "Sugar Shack",
    "Fizzy Lifting Drinks": "Sugar Shack",

    "Everlasting Gobstopper": "Secret Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Wonka Gum": "Secret Factory",

    "Hair Toffee": "The Other Factory",
    "Kazookles": "The Other Factory"
}

df["Factory Name"] = df["Product Name"].map(factory_mapping)

# Division Filter
st.sidebar.header("Dashboard Filters")

division_options = ["All"] + sorted(df["Division"].dropna().unique().tolist())

selected_division = st.sidebar.selectbox(
    "Select Division",
    division_options
)
# Date Range Filter
st.sidebar.subheader("Date Range")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Order Date"].min().date()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Order Date"].max().date()
)
# Product Search Filter
st.sidebar.subheader("Product Search")

search_product = st.sidebar.text_input(
    "Search Product Name",
    placeholder="Enter product name..."
)
# Margin Threshold Filter

min_margin = st.sidebar.slider(
    "Minimum Gross Margin (%)",
    min_value=0,
    max_value=100,
    value=0,
    step=5
)
# Apply Filter
# Apply Filters
if selected_division == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Division"] == selected_division]

filtered_df = filtered_df[
    (filtered_df["Order Date"].dt.date >= start_date) &
    (filtered_df["Order Date"].dt.date <= end_date)
]
# Apply Product Search
if search_product:
    filtered_df = filtered_df[
        filtered_df["Product Name"].str.contains(
            search_product,
            case=False,
            na=False
        )
    ]
# Apply Product-level Margin Filter

product_margins = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Gross Profit": "sum"
    })
)

product_margins["Gross Margin (%)"] = (
    product_margins["Gross Profit"] /
    product_margins["Sales"].replace(0, float("nan")) * 100
)

eligible_products = product_margins[
    product_margins["Gross Margin (%)"] >= min_margin
].index

filtered_df = filtered_df[
    filtered_df["Product Name"].isin(eligible_products)
]
# Average Shipping Duration by Ship Mode

st.subheader("🚚 Average Shipping Duration by Ship Mode")

shipping_mode_analysis = (
    filtered_df
    .groupby("Ship Mode")
    .agg(
        Average_Shipping_Days=("Shipping Days", "mean"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

shipping_mode_analysis["Average_Shipping_Days"] = (
    shipping_mode_analysis["Average_Shipping_Days"].round(2)
)

st.dataframe(
    shipping_mode_analysis,
    use_container_width=True,
    hide_index=True
)
# Region-wise Average Shipping Duration

st.subheader("🌍 Region-wise Average Shipping Duration")

region_shipping = (
    filtered_df
    .groupby("Region")
    .agg(
        Average_Shipping_Days=("Shipping Days", "mean"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region_shipping["Average_Shipping_Days"] = (
    region_shipping["Average_Shipping_Days"].round(2)
)

st.dataframe(
    region_shipping,
    use_container_width=True,
    hide_index=True
)
# Shipping Duration Distribution

st.subheader("📦 Shipping Duration Distribution")

fig = px.histogram(
    filtered_df,
    x="Shipping Days",
    nbins=10,
    title="Distribution of Shipping Duration",
    labels={"Shipping Days": "Shipping Duration (Days)"},
    color_discrete_sequence=["skyblue"]
)

fig.update_layout(
    xaxis_title="Shipping Duration (Days)",
    yaxis_title="Number of Orders",
    height=450
)

st.plotly_chart(fig, use_container_width=True)
# Shipping Performance Summary

st.subheader("🚚 Shipping Performance Summary")

overall_avg_shipping = filtered_df["Shipping Days"].mean()

mode_avg = (
    filtered_df.groupby("Ship Mode")["Shipping Days"]
    .mean()
    .dropna()
)

if not mode_avg.empty:
    fastest_mode = mode_avg.idxmin()
    slowest_mode = mode_avg.idxmax()
else:
    fastest_mode = "N/A"
    slowest_mode = "N/A"

total_shipping_orders = filtered_df["Order ID"].nunique()
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Shipping Days",
    f"{overall_avg_shipping:.2f}"
    if pd.notna(overall_avg_shipping)
    else "N/A"
)

col2.metric("Fastest Shipping Mode", fastest_mode)

col3.metric("Slowest Shipping Mode", slowest_mode)

col4.metric("Total Orders Analysed", total_shipping_orders)
# Shipping Data Quality Note

st.info("""
**Data Quality Note:** The source dataset which you provide me that contains unusually large
gaps between Order Date and Ship Date. The calculated shipping
duration is therefore much higher than normally expected.
These values have been preserved as provided in the original dataset.
Shipping duration results should be interpreted with this limitation
in mind.
""")
# Product Profitability Analysis

product_profit = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .reset_index()
    .sort_values(by="Gross Profit", ascending=False)
)
# Product Profitability Bar Chart

st.subheader("Product-wise Profit Analysis")

profit_chart = px.bar(
    product_profit.sort_values(
        by="Gross Profit",
        ascending=True
    ),
    x="Gross Profit",
    y="Product Name",
    orientation="h",
    title="Total Profit by Product",
    text_auto=",.2f",
    color="Gross Profit",
    color_continuous_scale="Blues"
)

profit_chart.update_layout(
    height=650,
    title_x=0.5,
    xaxis_title="Total Gross Profit",
    yaxis_title="",
    showlegend=False
)

profit_chart.update_traces(
    textposition="outside"
)

st.plotly_chart(profit_chart, width="stretch")
# Division Performance Analysis

division_performance = (
    filtered_df.groupby("Division")[["Sales", "Gross Profit"]]
    .sum()
    .reset_index()
)
# Division-wise Gross Margin

division_performance["Gross Margin (%)"] = (
    division_performance["Gross Profit"] /
    division_performance["Sales"] * 100
)
# Division-wise Sales vs Profit Chart

st.subheader("Division Performance Analysis")

division_chart = px.bar(
    division_performance,
    x="Division",
    y=["Sales", "Gross Profit"],
    barmode="group",
    title="Sales vs Profit by Division",
    text_auto=",.2f",
    color_discrete_sequence=["#3498DB", "#2ECC71"]
)

division_chart.update_layout(
    height=500,
    title_x=0.5,
    xaxis_title="Division",
    yaxis_title="Amount",
    legend_title="Financial Metrics"
)

st.plotly_chart(division_chart, width="stretch")
# Division-wise Gross Margin Chart

st.subheader("Gross Margin by Division")

margin_chart = px.bar(
    division_performance,
    x="Division",
    y="Gross Margin (%)",
    title="Gross Margin Comparison by Division",
    text_auto=".2f",
    color="Gross Margin (%)",
    color_continuous_scale="Greens"
)

margin_chart.update_layout(
    height=450,
    title_x=0.5,
    xaxis_title="Division",
    yaxis_title="Gross Margin (%)"
)

st.plotly_chart(margin_chart, width="stretch")
# Cost vs Margin Analysis

product_cost_analysis = (
    filtered_df.groupby("Product Name")
    .agg({
        "Sales": "sum",
        "Cost": "sum",
        "Gross Profit": "sum"
    })
    .reset_index()
)
product_cost_analysis["Gross Margin (%)"] = (
    product_cost_analysis["Gross Profit"] /
    product_cost_analysis["Sales"] * 100
)
# Apply Margin Threshold Filter

product_cost_analysis = product_cost_analysis[
    product_cost_analysis["Gross Margin (%)"] >= min_margin
]
# Margin Risk Classification

def classify_margin(margin):
    if margin >= 60:
        return "Healthy"
    elif margin >= 40:
        return "Moderate"
    else:
        return "Low Margin"

product_cost_analysis["Risk Status"] = (
    product_cost_analysis["Gross Margin (%)"]
    .apply(classify_margin)
)
# Risk Summary

healthy_count = (
    product_cost_analysis["Risk Status"] == "Healthy"
).sum()

moderate_count = (
    product_cost_analysis["Risk Status"] == "Moderate"
).sum()

low_margin_count = (
    product_cost_analysis["Risk Status"] == "Low Margin"
).sum()

st.subheader("Margin Risk Summary")

risk_col1, risk_col2, risk_col3 = st.columns(3)

risk_col1.metric("Healthy Products", healthy_count)
risk_col2.metric("Moderate Products", moderate_count)
risk_col3.metric("Low Margin Products", low_margin_count)
# Margin Risk Report

st.subheader("Product Margin Risk Report")

risk_report = product_cost_analysis[
    ["Product Name", "Sales", "Cost",
     "Gross Profit", "Gross Margin (%)", "Risk Status"]
].sort_values(by="Gross Margin (%)", ascending=True)

st.dataframe(
    risk_report,
    width="stretch",
    hide_index=True,
    column_config={
        "Product Name": st.column_config.TextColumn(width="large"),
        "Gross Margin (%)": st.column_config.NumberColumn(
            format="%.2f%%"
        ),
        "Sales": st.column_config.NumberColumn(format="%.2f"),
        "Cost": st.column_config.NumberColumn(format="%.2f"),
        "Gross Profit": st.column_config.NumberColumn(format="%.2f")
    }
)
# Highest and Lowest Margin Products Ranking

st.subheader("🏆 Highest & Lowest Margin Products")

if not product_cost_analysis.empty:

    # Top 5 highest margin products
    highest_margin = product_cost_analysis.sort_values(
        by="Gross Margin (%)",
        ascending=False
    ).head(5)

    # Top 5 lowest margin products
    lowest_margin = product_cost_analysis.sort_values(
        by="Gross Margin (%)",
        ascending=True
    ).head(5)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🟢 Top 5 Highest Margin")
        st.dataframe(
            highest_margin[
                ["Product Name", "Sales", "Gross Profit", "Gross Margin (%)"]
            ].style.format({
                "Sales": "{:.2f}",
                "Gross Profit": "{:.2f}",
                "Gross Margin (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.markdown("### 🔴 Top 5 Lowest Margin")
        st.dataframe(
            lowest_margin[
                ["Product Name", "Sales", "Gross Profit", "Gross Margin (%)"]
            ].style.format({
                "Sales": "{:.2f}",
                "Gross Profit": "{:.2f}",
                "Gross Margin (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning("No product data available for the selected filters.")
# Product-wise Sales vs Cost Comparison

st.subheader("📊 Product-wise Sales vs Cost Comparison")

if not product_cost_analysis.empty:

    cost_sales_chart = product_cost_analysis.melt(
        id_vars=["Product Name"],
        value_vars=["Sales", "Cost"],
        var_name="Metric",
        value_name="Amount"
    )

    fig_cost_sales = px.bar(
        cost_sales_chart,
        x="Amount",
        y="Product Name",
        color="Metric",
        barmode="group",
        orientation="h",
        title="Product-wise Sales vs Cost Comparison",
        labels={
            "Amount": "Total Amount",
            "Product Name": "Product",
            "Metric": "Financial Metric"
        },
        color_discrete_map={
            "Sales": "#3498DB",
            "Cost": "#E67E22"
        }
    )

    fig_cost_sales.update_layout(
        height=700,
        yaxis={"categoryorder": "total ascending"},
        legend_title="Metric"
    )

    st.plotly_chart(
        fig_cost_sales,
        use_container_width=True
    )

else:
    st.warning("No product data available for the selected filters.")
# Cost-Heavy and Margin-Poor Product Analysis

st.subheader("⚠️ Cost-Heavy & Margin-Poor Products")

if not product_cost_analysis.empty:

    risk_analysis = product_cost_analysis.copy()

    # Calculate Cost Ratio
    risk_analysis["Cost Ratio (%)"] = (
        risk_analysis["Cost"] / risk_analysis["Sales"] * 100
    )

    # Identify product risk
    def identify_product_risk(row):

        if row["Cost Ratio (%)"] >= 60 and row["Gross Margin (%)"] < 40:
            return "High Cost & Low Margin"

        elif row["Cost Ratio (%)"] >= 60:
            return "Cost-Heavy"

        elif row["Gross Margin (%)"] < 40:
            return "Low Margin"

        else:
            return "Normal"

    risk_analysis["Product Risk"] = risk_analysis.apply(
        identify_product_risk,
        axis=1
    )

    # Show only products requiring attention
    flagged_products = risk_analysis[
        risk_analysis["Product Risk"] != "Normal"
    ].sort_values(
        by="Cost Ratio (%)",
        ascending=False
    )

    if not flagged_products.empty:

        st.markdown("### Products Requiring Attention")

        st.dataframe(
            flagged_products[
                [
                    "Product Name",
                    "Sales",
                    "Cost",
                    "Gross Margin (%)",
                    "Cost Ratio (%)",
                    "Product Risk"
                ]
            ].style.format({
                "Sales": "{:.2f}",
                "Cost": "{:.2f}",
                "Gross Margin (%)": "{:.2f}%",
                "Cost Ratio (%)": "{:.2f}%"
            }),
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No cost-heavy or low-margin products found.")

else:
    st.warning("No product data available for the selected filters.")
# Factory-wise Performance Analysis

st.subheader("🏭 Factory-wise Performance Analysis")

factory_performance = (
    filtered_df
    .groupby("Factory Name")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

factory_performance["Gross Margin (%)"] = (
    factory_performance["Total_Profit"]
    / factory_performance["Total_Sales"] * 100
)

factory_performance = factory_performance.sort_values(
    by="Total_Profit",
    ascending=False
)

st.dataframe(
    factory_performance.style.format({
        "Total_Sales": "{:,.2f}",
        "Total_Profit": "{:,.2f}",
        "Total_Cost": "{:,.2f}",
        "Total_Units": "{:,.0f}",
        "Total_Orders": "{:,.0f}",
        "Gross Margin (%)": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
# Factory-wise Gross Profit Comparison

st.markdown("### 📊 Factory-wise Gross Profit Comparison")

fig_factory_profit = px.bar(
    factory_performance,
    x="Factory Name",
    y="Total_Profit",
    color="Gross Margin (%)",
    text="Total_Profit",
    color_continuous_scale="RdYlGn",
    title="Gross Profit Generated by Each Factory"
)

fig_factory_profit.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_factory_profit.update_layout(
    height=500,
    xaxis_title="Factory",
    yaxis_title="Total Gross Profit",
    showlegend=False
)

st.plotly_chart(
    fig_factory_profit,
    use_container_width=True
)
# Factory-wise Sales vs Profit Comparison

st.markdown("### 📈 Factory-wise Sales vs Profit")

factory_comparison = factory_performance.melt(
    id_vars=["Factory Name"],
    value_vars=["Total_Sales", "Total_Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_factory_comparison = px.bar(
    factory_comparison,
    x="Factory Name",
    y="Amount",
    color="Metric",
    barmode="group",
    text="Amount",
    title="Factory-wise Sales vs Gross Profit",
    color_discrete_map={
        "Total_Sales": "#3498DB",
        "Total_Profit": "#E67E22"
    }
)

fig_factory_comparison.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_factory_comparison.update_layout(
    height=550,
    xaxis_title="Factory",
    yaxis_title="Amount",
    legend_title="Metric"
)

st.plotly_chart(
    fig_factory_comparison,
    use_container_width=True
)
# Factory-wise Gross Margin Analysis

st.markdown("### 📊 Factory-wise Gross Margin Comparison")

fig_factory_margin = px.bar(
    factory_performance.sort_values(
        by="Gross Margin (%)",
        ascending=True
    ),
    x="Gross Margin (%)",
    y="Factory Name",
    orientation="h",
    color="Gross Margin (%)",
    text="Gross Margin (%)",
    color_continuous_scale="RdYlGn",
    title="Gross Margin Percentage by Factory"
)

fig_factory_margin.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_factory_margin.update_layout(
    height=500,
    xaxis_title="Gross Margin (%)",
    yaxis_title="Factory",
    showlegend=False
)

st.plotly_chart(
    fig_factory_margin,
    use_container_width=True
)
# Factory Performance Summary

st.markdown("### 🏆 Factory Performance Summary")

if not factory_performance.empty:

    best_profit_factory = factory_performance.loc[
        factory_performance["Total_Profit"].idxmax()
    ]

    best_margin_factory = factory_performance.loc[
        factory_performance["Gross Margin (%)"].idxmax()
    ]

    lowest_margin_factory = factory_performance.loc[
        factory_performance["Gross Margin (%)"].idxmin()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Highest Profit Factory",
            best_profit_factory["Factory Name"],
            f"{best_profit_factory['Total_Profit']:,.2f}"
        )

    with col2:
        st.metric(
            "Highest Margin Factory",
            best_margin_factory["Factory Name"],
            f"{best_margin_factory['Gross Margin (%)']:.2f}%"
        )

    with col3:
        st.metric(
            "Lowest Margin Factory",
            lowest_margin_factory["Factory Name"],
            f"{lowest_margin_factory['Gross Margin (%)']:.2f}%"
        )
# Region-wise Performance Analysis

st.subheader("🌎 Region-wise Performance Analysis")

region_performance = (
    filtered_df
    .groupby("Region")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

region_performance["Gross Margin (%)"] = (
    region_performance["Total_Profit"]
    / region_performance["Total_Sales"] * 100
)

region_performance = region_performance.sort_values(
    by="Total_Sales",
    ascending=False
)

st.dataframe(
    region_performance.style.format({
        "Total_Sales": "{:,.2f}",
        "Total_Profit": "{:,.2f}",
        "Total_Cost": "{:,.2f}",
        "Total_Units": "{:,.0f}",
        "Total_Orders": "{:,.0f}",
        "Gross Margin (%)": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
# Region-wise Sales vs Profit Chart

st.markdown("### 📊 Region-wise Sales vs Profit")

region_chart_data = region_performance.melt(
    id_vars=["Region"],
    value_vars=["Total_Sales", "Total_Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_region = px.bar(
    region_chart_data,
    x="Region",
    y="Amount",
    color="Metric",
    barmode="group",
    text="Amount",
    title="Region-wise Sales vs Gross Profit",
    color_discrete_map={
        "Total_Sales": "#3498DB",
        "Total_Profit": "#E67E22"
    }
)

fig_region.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_region.update_layout(
    height=500,
    xaxis_title="Region",
    yaxis_title="Amount",
    legend_title="Metric"
)

st.plotly_chart(fig_region, use_container_width=True)
# State-wise Performance Analysis

st.subheader("🗺️ State-wise Performance Analysis")

state_performance = (
    filtered_df
    .groupby("State/Province")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Cost=("Cost", "sum"),
        Total_Units=("Units", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
)

state_performance["Gross Margin (%)"] = (
    state_performance["Total_Profit"]
    / state_performance["Total_Sales"] * 100
)

state_performance = state_performance.sort_values(
    by="Total_Sales",
    ascending=False
)

st.dataframe(
    state_performance.style.format({
        "Total_Sales": "{:,.2f}",
        "Total_Profit": "{:,.2f}",
        "Total_Cost": "{:,.2f}",
        "Total_Units": "{:,.0f}",
        "Total_Orders": "{:,.0f}",
        "Gross Margin (%)": "{:.2f}%"
    }),
    use_container_width=True,
    hide_index=True
)
# Top 10 States by Sales

st.markdown("### 🏆 Top 10 States by Sales")

top_10_states = state_performance.nlargest(
    10, "Total_Sales"
).sort_values(
    by="Total_Sales",
    ascending=True
)

fig_top_states = px.bar(
    top_10_states,
    x="Total_Sales",
    y="State/Province",
    orientation="h",
    color="Total_Sales",
    text="Total_Sales",
    color_continuous_scale="Blues",
    title="Top 10 States by Total Sales"
)

fig_top_states.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_top_states.update_layout(
    height=600,
    xaxis_title="Total Sales",
    yaxis_title="State"
)

st.plotly_chart(
    fig_top_states,
    use_container_width=True
)
# Top 10 States by Gross Profit

st.markdown("### 🏆 Top 10 States by Gross Profit")

top_10_profit_states = state_performance.nlargest(
    10, "Total_Profit"
).sort_values(
    by="Total_Profit",
    ascending=True
)

fig_state_profit = px.bar(
    top_10_profit_states,
    x="Total_Profit",
    y="State/Province",
    orientation="h",
    color="Total_Profit",
    text="Total_Profit",
    color_continuous_scale="Greens",
    title="Top 10 States by Gross Profit"
)

fig_state_profit.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig_state_profit.update_layout(
    height=600,
    xaxis_title="Total Gross Profit",
    yaxis_title="State"
)

st.plotly_chart(
    fig_state_profit,
    use_container_width=True
)
# Region and State Performance Summary

st.markdown("### 🏆 Region & State Performance Summary")

if not region_performance.empty and not state_performance.empty:

    best_sales_region = region_performance.loc[
        region_performance["Total_Sales"].idxmax()
    ]

    best_profit_region = region_performance.loc[
        region_performance["Total_Profit"].idxmax()
    ]

    best_sales_state = state_performance.loc[
        state_performance["Total_Sales"].idxmax()
    ]

    best_profit_state = state_performance.loc[
        state_performance["Total_Profit"].idxmax()
    ]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Highest Sales Region",
            best_sales_region["Region"],
            f"{best_sales_region['Total_Sales']:,.2f}"
        )

        st.metric(
            "Highest Sales State",
            best_sales_state["State/Province"],
            f"{best_sales_state['Total_Sales']:,.2f}"
        )

    with col2:
        st.metric(
            "Highest Profit Region",
            best_profit_region["Region"],
            f"{best_profit_region['Total_Profit']:,.2f}"
        )

        st.metric(
            "Highest Profit State",
            best_profit_state["State/Province"],
            f"{best_profit_state['Total_Profit']:,.2f}"
        )
# Monthly Sales & Profit Trends

st.header("📈 Monthly Sales & Profit Trends")

monthly_analysis = (
    filtered_df
    .assign(Month=filtered_df["Order Date"].dt.to_period("M").astype(str))
    .groupby("Month")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .reset_index()
)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=monthly_analysis["Month"],
    y=monthly_analysis["Total_Sales"],
    mode="lines+markers",
    name="Monthly Sales"
))

fig.add_trace(go.Scatter(
    x=monthly_analysis["Month"],
    y=monthly_analysis["Total_Profit"],
    mode="lines+markers",
    name="Monthly Profit"
))

fig.update_layout(
    title="Monthly Sales vs Gross Profit",
    xaxis_title="Month",
    yaxis_title="Amount",
    height=500,
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
# Units Sold Analysis

st.header("📦 Units Sold Analysis")

units_analysis = (
    filtered_df
    .groupby("Product Name")
    .agg(Total_Units=("Units", "sum"))
    .reset_index()
    .sort_values("Total_Units", ascending=False)
)

fig = px.bar(
    units_analysis.head(10),
    x="Total_Units",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Units Sold",
    text="Total_Units"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    xaxis_title="Total Units Sold",
    yaxis_title="Product",
    height=500
)

st.plotly_chart(fig, use_container_width=True)
# Division-wise Units Sold Analysis

st.subheader("Division-wise Units Sold")

division_units = (
    filtered_df
    .groupby("Division")
    .agg(Total_Units=("Units", "sum"))
    .reset_index()
    .sort_values("Total_Units", ascending=False)
)

fig = px.bar(
    division_units,
    x="Division",
    y="Total_Units",
    color="Division",
    text="Total_Units",
    title="Units Sold by Division"
)

fig.update_layout(
    xaxis_title="Division",
    yaxis_title="Total Units Sold",
    height=450
)

st.plotly_chart(fig, use_container_width=True)
# Customer Analysis

st.header("👥 Customer Analysis")

# Customer-wise Performance
customer_sales = (
    filtered_df
    .groupby("Customer ID")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum"),
        Total_Orders=("Order ID", "nunique")
    )
    .reset_index()
    .sort_values("Total_Sales", ascending=False)
)

# Top 10 Customers by Sales
st.subheader("Top 10 Customers by Sales")

top_customers_sales = customer_sales.head(10).copy()

top_customers_sales["Customer ID"] = (
    top_customers_sales["Customer ID"].astype(str)
)

fig = px.bar(
    top_customers_sales,
    x="Customer ID",
    y="Total_Sales",
    color="Total_Sales",
    text="Total_Sales",
    title="Top 10 Customers by Sales",
    labels={
        "Customer ID": "Customer ID",
        "Total_Sales": "Total Sales"
    }
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Total Sales",
    xaxis_tickangle=-45,
    height=550,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
# Top 10 Customers by Profit

st.subheader("🏆 Top 10 Customers by Profit")

top_customers_profit = (
    customer_sales
    .sort_values("Total_Profit", ascending=False)
    .head(10)
    .copy()
)

fig = px.bar(
    top_customers_profit,
    x="Customer ID",
    y="Total_Profit",
    color="Total_Profit",
    text="Total_Profit",
    title="Top 10 Customers by Profit",
    labels={
        "Customer ID": "Customer ID",
        "Total_Profit": "Total Profit"
    }
)

fig.update_traces(
    texttemplate="%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Total Profit",
    xaxis_tickangle=-45,
    height=550,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
# Customer-wise Order Count

st.subheader("📊 Customer-wise Order Count")

customer_orders = (
    customer_sales
    .sort_values("Total_Orders", ascending=False)
    .head(10)
    .copy()
)

customer_orders["Customer ID"] = (
    customer_orders["Customer ID"].astype(str)
)

fig = px.bar(
    customer_orders,
    x="Customer ID",
    y="Total_Orders",
    color="Total_Orders",
    text="Total_Orders",
    title="Top 10 Customers by Number of Orders",
    labels={
        "Customer ID": "Customer ID",
        "Total_Orders": "Number of Orders"
    }
)

fig.update_traces(
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Number of Orders",
    xaxis_tickangle=-45,
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
# Customer Average Order Value

st.subheader("💰 Customer Average Order Value")

customer_sales["Average_Order_Value"] = (
    customer_sales["Total_Sales"] /
    customer_sales["Total_Orders"].replace(0, float("nan"))
)

top_aov_customers = (
    customer_sales
    .sort_values("Average_Order_Value", ascending=False)
    .head(10)
    .copy()
)

top_aov_customers["Customer ID"] = (
    top_aov_customers["Customer ID"].astype(str)
)

fig = px.bar(
    top_aov_customers,
    x="Customer ID",
    y="Average_Order_Value",
    color="Average_Order_Value",
    text="Average_Order_Value",
    title="Top 10 Customers by Average Order Value",
    labels={
        "Customer ID": "Customer ID",
        "Average_Order_Value": "Average Order Value"
    }
)

fig.update_traces(
    texttemplate="%{text:,.2f}",
    textposition="outside"
)

fig.update_layout(
    xaxis_title="Customer ID",
    yaxis_title="Average Order Value",
    xaxis_tickangle=-45,
    height=550,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)
# Business Recommendations

st.header("💡 Business Recommendations")

st.markdown("""
### 1. Focus on High-Profit Products
Prioritize products that generate strong sales and healthy
gross margins to maintain overall profitability.

### 2. Review Low-Margin Products
Investigate products with high costs and low gross margins.
Explore cost optimization and pricing improvements.

### 3. Strengthen Chocolate Division
Chocolate contributes the largest share of total profit.
Maintain product quality and monitor its cost performance.

### 4. Improve Factory Performance
Compare factory-wise sales, profit and gross margins.
Identify opportunities to improve weaker-performing factories.

### 5. Monitor Customer Performance
Identify high-value customers and understand their purchasing
patterns to support customer retention.

### 6. Validate Shipping Date Data
The source dataset contains unusually large gaps between
Order Date and Ship Date. Verify these dates before making
shipping efficiency decisions.
""")
# Profit Concentration Analysis

st.subheader("Profit Concentration Analysis")

pareto_data = (
    filtered_df.groupby("Product Name")["Gross Profit"]
    .sum()
    .reset_index()
    .sort_values(by="Gross Profit", ascending=False)
)

# Calculate Cumulative Profit
pareto_data["Cumulative Profit"] = (
    pareto_data["Gross Profit"].cumsum()
)

# Calculate Cumulative Profit Percentage
total_pareto_profit = pareto_data["Gross Profit"].sum()

if total_pareto_profit > 0:
    pareto_data["Cumulative Profit (%)"] = (
        pareto_data["Cumulative Profit"] /
        total_pareto_profit * 100
    )
else:
    pareto_data["Cumulative Profit (%)"] = 0
# 80% Profit Concentration KPI

if total_pareto_profit > 0:
    products_for_80_percent = (
        (pareto_data["Cumulative Profit (%)"] < 80).sum() + 1
    )
else:
    products_for_80_percent = 0

st.metric(
    "Products Required for 80% Profit",
    products_for_80_percent
)
# Pareto Chart

fig = make_subplots(specs=[[{"secondary_y": True}]])

# Profit Bars
fig.add_trace(
    go.Bar(
        x=pareto_data["Product Name"],
        y=pareto_data["Gross Profit"],
        name="Gross Profit",
        marker_color="#3498DB"
    ),
    secondary_y=False
)

# Cumulative Profit Line
fig.add_trace(
    go.Scatter(
        x=pareto_data["Product Name"],
        y=pareto_data["Cumulative Profit (%)"],
        name="Cumulative Profit (%)",
        mode="lines+markers",
        line=dict(color="#E67E22", width=3)
    ),
    secondary_y=True
)

fig.update_layout(
    title="Product-wise Profit Pareto Analysis",
    title_x=0.5,
    height=750,
    xaxis_title="Products",
    legend_title="Metrics",
    hovermode="x unified"
)

fig.update_yaxes(
    title_text="Gross Profit",
    secondary_y=False
)

fig.update_yaxes(
    title_text="Cumulative Profit (%)",
    secondary_y=True,
    range=[0, 110]
)

st.plotly_chart(fig, width="stretch")
# Revenue Concentration Analysis

st.subheader("Revenue Concentration Analysis")

revenue_pareto = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .reset_index()
    .sort_values(by="Sales", ascending=False)
)

# Calculate Cumulative Revenue
revenue_pareto["Cumulative Revenue"] = (
    revenue_pareto["Sales"].cumsum()
)

# Calculate Cumulative Revenue Percentage
total_revenue = revenue_pareto["Sales"].sum()

if total_revenue > 0:
    revenue_pareto["Cumulative Revenue (%)"] = (
        revenue_pareto["Cumulative Revenue"] /
        total_revenue * 100
    )
else:
    revenue_pareto["Cumulative Revenue (%)"] = 0
# Revenue Pareto Chart

revenue_fig = make_subplots(
    specs=[[{"secondary_y": True}]]
)
# 80% Revenue Concentration KPI

if total_revenue > 0:
    products_for_80_revenue = (
        (revenue_pareto["Cumulative Revenue (%)"] < 80).sum() + 1
    )
else:
    products_for_80_revenue = 0

st.metric(
    "Products Required for 80% Revenue",
    products_for_80_revenue
)
# Revenue Bars
revenue_fig.add_trace(
    go.Bar(
        x=revenue_pareto["Product Name"],
        y=revenue_pareto["Sales"],
        name="Total Revenue",
        marker_color="#3498DB"
    ),
    secondary_y=False
)

# Cumulative Revenue Line
revenue_fig.add_trace(
    go.Scatter(
        x=revenue_pareto["Product Name"],
        y=revenue_pareto["Cumulative Revenue (%)"],
        name="Cumulative Revenue (%)",
        mode="lines+markers",
        line=dict(color="#E67E22", width=3)
    ),
    secondary_y=True
)

revenue_fig.update_layout(
    title="Product-wise Revenue Pareto Analysis",
    title_x=0.5,
    height=750,
    xaxis_title="Products",
    legend_title="Metrics",
    hovermode="x unified"
)

revenue_fig.update_yaxes(
    title_text="Total Revenue",
    secondary_y=False
)

revenue_fig.update_yaxes(
    title_text="Cumulative Revenue (%)",
    secondary_y=True,
    range=[0, 110]
)

st.plotly_chart(revenue_fig, width="stretch")
# Product-wise Cost vs Sales Comparison

st.subheader("Product-wise Cost vs Sales Comparison")

cost_sales_data = product_cost_analysis.melt(
    id_vars=["Product Name"],
    value_vars=["Cost", "Sales"],
    var_name="Metric",
    value_name="Amount"
)

product_order = (
    product_cost_analysis
    .sort_values("Sales", ascending=True)["Product Name"]
    .tolist()
)

cost_chart = px.bar(
    cost_sales_data,
    x="Amount",
    y="Product Name",
    color="Metric",
    barmode="group",
    orientation="h",
    text_auto=",.0f",
    title="Total Cost vs Total Sales by Product",
    category_orders={
        "Product Name": product_order
    },
    color_discrete_map={
        "Cost": "#F39C12",
        "Sales": "#3498DB"
    }
)

cost_chart.update_layout(
    height=750,
    title_x=0.5,
    xaxis_title="Amount",
    yaxis_title="",
    legend_title="Financial Metric",
    margin=dict(l=220, r=60, t=80, b=60)
)

cost_chart.update_traces(
    textposition="outside"
)

st.plotly_chart(cost_chart, width="stretch")

# Display dataset
st.subheader("Dataset Preview")
# Calculate KPIs
total_sales =  filtered_df["Sales"].sum()
total_profit = filtered_df["Gross Profit"].sum()
total_units =  filtered_df["Units"].sum()
gross_margin = (total_profit / total_sales) * 100
total_orders = filtered_df["Order ID"].nunique()
# Additional Business Metrics

profit_per_unit = (
    total_profit / total_units if total_units > 0 else 0
)

revenue_contribution = (
    total_sales / df["Sales"].sum() * 100
    if df["Sales"].sum() > 0 else 0
)

profit_contribution = (
    total_profit / df["Gross Profit"].sum() * 100
    if df["Gross Profit"].sum() > 0 else 0
)
# KPI Cards
st.subheader("Business Performance Overview")

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Sales", f"{total_sales:,.2f}")
col2.metric("Total Profit", f"{total_profit:,.2f}")
col3.metric("Units Sold", f"{total_units:,}")
col4.metric("Gross Margin", f"{gross_margin:.2f}%")
col5.metric("Total Orders", f"{total_orders:,}")
# Additional KPI Cards
st.subheader("Advanced Business Metrics")

col6, col7, col8 = st.columns(3)

col6.metric("Profit Per Unit", f"{profit_per_unit:.2f}")
col7.metric("Revenue Contribution", f"{revenue_contribution:.2f}%")
col8.metric("Profit Contribution", f"{profit_contribution:.2f}%")

st.dataframe(
    filtered_df,
    width="stretch",
    height=500,
    column_config={
        "Division": st.column_config.TextColumn(width="medium"),
        "Region": st.column_config.TextColumn(width="medium"),
        "Product Name": st.column_config.TextColumn(width="large")
    }
)
             