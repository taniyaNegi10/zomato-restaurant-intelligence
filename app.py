
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st



# 1. PAGE CONFIGURATION


st.set_page_config(
    page_title="Zomato Restaurant Intelligence",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)



# 2. THEME CONFIGURATION


BG_COLOR = "#F8F5F0"
CARD_COLOR = "#FFFFFF"
PRIMARY_COLOR = "#E85D4A"
DARK_COLOR = "#292524"
MUTED_COLOR = "#78716C"
BORDER_COLOR = "#EEE7DF"

CHART_COLORS = [
    "#E85D4A",
    "#F4A261",
    "#6D8B74",
    "#547AA5",
    "#B08BBB"
]

SENTIMENT_COLORS = {
    "Positive": "#6D8B74",
    "Negative": "#E85D4A",
    "Neutral": "#F4A261"
}


# 3. PROJECT PATHS AND DATA LOADING


PROJECT_ROOT = Path(__file__).resolve().parent

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "restaurant_intelligence.csv"
)


@st.cache_data
def load_data():

    data = pd.read_csv(DATA_PATH)

    required_columns = [
        "Name",
        "Cost",
        "Cuisine_Count",
        "Collection_Count",
        "Cluster",
        "Total_Reviews",
        "Positive_Reviews",
        "Negative_Reviews",
        "Neutral_Reviews",
        "Positive_Percentage"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    numeric_columns = [
        "Cost",
        "Cuisine_Count",
        "Collection_Count",
        "Cluster",
        "Total_Reviews",
        "Positive_Reviews",
        "Negative_Reviews",
        "Neutral_Reviews",
        "Positive_Percentage"
    ]

    for column in numeric_columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )

    # Restaurants without matching reviews have zero review counts.
    # Their sentiment percentage remains missing.

    review_count_columns = [
        "Total_Reviews",
        "Positive_Reviews",
        "Negative_Reviews",
        "Neutral_Reviews"
    ]

    data[review_count_columns] = (
        data[review_count_columns].fillna(0)
    )

    return data


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "Dashboard dataset not found. "
        "Please check data/processed/"
    )

    st.stop()

except ValueError as error:

    st.error(str(error))
    st.stop()



# 4. PREMIUM CUSTOM CSS


st.markdown("""
<style>

/* Main application background */

.stApp {
    background-color: #F8F5F0;
    color: #292524;
    font-family: 'Inter', 'Segoe UI', sans-serif;
}

/* Main content spacing */

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #EEE7DF;
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 2rem;
}

/* Sidebar branding */

[data-testid="stSidebar"] h1 {
    color: #292524 !important;
    font-size: 1.45rem !important;
    font-weight: 750 !important;
}

/* Sidebar navigation */

[data-testid="stSidebar"] [data-testid="stRadio"] label {
    color: #57534E;
    font-size: 0.92rem;
    font-weight: 500;
    padding: 10px 12px;
    border-radius: 10px;
    transition: all 0.2s ease;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background-color: #FFF1ED;
    color: #E85D4A;
}

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
    background-color: #FCEAE6;
    color: #D94B39;
    font-weight: 650;
}

/* Main headings */

h1 {
    color: #292524 !important;
    font-size: 2.15rem !important;
    font-weight: 750 !important;
    letter-spacing: -0.8px;
}

h2 {
    color: #292524 !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
}

h3 {
    color: #44403C !important;
    font-size: 1.12rem !important;
    font-weight: 650 !important;
}

/* Supporting text */

.stCaption {
    color: #78716C !important;
}

/* KPI cards */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    padding: 23px 22px;
    border: 1px solid #EEE7DF;
    border-radius: 16px;
    box-shadow: 0 3px 12px rgba(41, 37, 36, 0.035);
    transition: all 0.2s ease;
}

div[data-testid="stMetric"]:hover {
    border-color: #E85D4A;
    box-shadow: 0 5px 18px rgba(232, 93, 74, 0.09);
}

div[data-testid="stMetricLabel"] {
    color: #78716C !important;
    font-size: 0.86rem !important;
    font-weight: 500 !important;
}

div[data-testid="stMetricValue"] {
    color: #292524 !important;
    font-size: 1.85rem !important;
    font-weight: 750 !important;
}

/* Data tables */

[data-testid="stDataFrame"] {
    background-color: #FFFFFF;
    border: 1px solid #EEE7DF;
    border-radius: 12px;
    overflow: hidden;
}

/* Chart containers */

[data-testid="stPlotlyChart"] {
    background: #FFFFFF;
    border: 1px solid #EEE7DF;
    border-radius: 15px;
    padding: 12px;
}

/* Input controls */

.stSelectbox > div > div {
    border-radius: 10px;
}

/* Buttons */

.stButton > button {
    background-color: #E85D4A;
    color: #FFFFFF;
    border: none;
    border-radius: 10px;
    font-weight: 600;
    padding: 0.55rem 1.2rem;
}

.stButton > button:hover {
    background-color: #D94B39;
    color: #FFFFFF;
    border: none;
}

/* Dividers */

hr {
    border-color: #E9E1D8;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Streamlit header */

[data-testid="stHeader"] {
    background-color: transparent;
}

</style>
""", unsafe_allow_html=True)


# 5. CHART STYLING FUNCTION


def style_chart(fig):

    fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",

        font=dict(
            family="Inter, Segoe UI, sans-serif",
            color=DARK_COLOR,
            size=12
        ),

        title=dict(
            font=dict(
                size=17,
                color=DARK_COLOR
            ),
            x=0.03
        ),

        height=400,

        margin=dict(
            l=30,
            r=25,
            t=65,
            b=65
        ),

        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.16,
            xanchor="center",
            x=0.5,
            bgcolor="rgba(255,255,255,0)"
        ),

        hoverlabel=dict(
            bgcolor="white",
            font_color=DARK_COLOR
        )
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="#F0ECE6",
        zeroline=False
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="#F0ECE6",
        zeroline=False
    )

    return fig



# 6. SIDEBAR NAVIGATION


st.sidebar.title("🍽️ Zomato Insights")

st.sidebar.caption(
    "RESTAURANT INTELLIGENCE PLATFORM"
)

st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Overview",
        "Restaurant Analytics",
        "Customer Sentiment",
        "Restaurant Clustering",
        "Business Insights"
    ]
)

st.sidebar.divider()

st.sidebar.markdown(
    """
    <div style="
        color: #78716C;
        font-size: 12px;
        line-height: 1.7;
    ">
        <b>Zomato Intelligence</b><br>
        Powered by Python, Machine Learning,
        NLP and Streamlit.
    </div>
    """,
    unsafe_allow_html=True
)



# 7. OVERVIEW PAGE


if page == "Overview":

    st.title("Restaurant Intelligence Dashboard")

    st.caption(
        "Explore restaurant performance, customer sentiment "
        "and market segments."
    )

    # Calculate business metrics

    total_restaurants = df["Name"].nunique()

    avg_cost = df["Cost"].mean()

    total_reviews = df["Total_Reviews"].sum()

    total_positive = df["Positive_Reviews"].sum()

    overall_positive = (
        total_positive / total_reviews * 100
        if total_reviews > 0 else 0
    )

    # KPI Cards

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Restaurants",
        f"{total_restaurants:,}"
    )

    col2.metric(
        "Average Cost",
        f"₹{avg_cost:,.0f}"
    )

    col3.metric(
        "Customer Reviews",
        f"{total_reviews:,.0f}"
    )

    col4.metric(
        "Positive Sentiment",
        f"{overall_positive:.1f}%"
    )

    st.divider()

    left, right = st.columns(2)

    # Cluster Distribution

    with left:

        st.subheader("Restaurant Cluster Distribution")

        cluster_counts = (
            df["Cluster"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        cluster_counts.columns = [
            "Cluster",
            "Restaurants"
        ]

        cluster_counts["Cluster"] = (
            cluster_counts["Cluster"].astype(str)
        )

        fig = px.pie(
            cluster_counts,
            names="Cluster",
            values="Restaurants",
            hole=0.58,
            title="Restaurant Segments",
            color_discrete_sequence=CHART_COLORS
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch"
        )

    # Sentiment Distribution

    with right:

        st.subheader("Customer Sentiment Distribution")

        sentiment_data = pd.DataFrame({
            "Sentiment": [
                "Positive",
                "Negative",
                "Neutral"
            ],
            "Reviews": [
                df["Positive_Reviews"].sum(),
                df["Negative_Reviews"].sum(),
                df["Neutral_Reviews"].sum()
            ]
        })

        fig = px.bar(
            sentiment_data,
            x="Sentiment",
            y="Reviews",
            color="Sentiment",
            title="Review Sentiment",
            color_discrete_map=SENTIMENT_COLORS
        )

        fig.update_traces(
            marker_line_width=0,
            opacity=0.9
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch"
        )


# 8. RESTAURANT ANALYTICS PAGE


elif page == "Restaurant Analytics":

    st.title("Restaurant Analytics")

    st.caption(
        "Explore restaurant costs, cuisine diversity "
        "and restaurant collections."
    )

    max_cost = int(df["Cost"].max())

    cost_range = st.slider(
        "Filter by restaurant cost",
        min_value=0,
        max_value=max_cost,
        value=(0, max_cost),
        step=50
    )

    filtered = df[
        df["Cost"].between(
            cost_range[0],
            cost_range[1]
        )
    ].copy()

    st.write(
        f"Restaurants found: **{len(filtered)}**"
    )

    if filtered.empty:

        st.info(
            "No restaurants found in this cost range."
        )

    else:

        filtered["Cluster_Label"] = (
            filtered["Cluster"].astype(str)
        )

        fig = px.scatter(
            filtered,
            x="Cuisine_Count",
            y="Cost",
            color="Cluster_Label",
            hover_name="Name",
            size="Collection_Count",
            size_max=25,
            title="Restaurant Cost vs Cuisine Diversity",
            color_discrete_sequence=CHART_COLORS,
            labels={
                "Cuisine_Count": "Number of Cuisines",
                "Cost": "Average Cost (₹)",
                "Cluster_Label": "Restaurant Cluster",
                "Collection_Count": "Collections"
            }
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch"
        )

    st.divider()

    st.subheader("Restaurant Directory")

    st.dataframe(
        filtered[
            [
                "Name",
                "Cost",
                "Cuisine_Count",
                "Collection_Count",
                "Cluster"
            ]
        ],
        width="stretch",
        hide_index=True
    )



# 9. CUSTOMER SENTIMENT PAGE


elif page == "Customer Sentiment":

    st.title("Customer Sentiment Analysis")

    st.caption(
        "Understand customer feedback using "
        "VADER-based sentiment analysis."
    )

    total = df["Total_Reviews"].sum()

    positive = df["Positive_Reviews"].sum()

    negative = df["Negative_Reviews"].sum()

    neutral = df["Neutral_Reviews"].sum()

    positive_percentage = (
        positive / total * 100
        if total > 0 else 0
    )

    negative_percentage = (
        negative / total * 100
        if total > 0 else 0
    )

    neutral_percentage = (
        neutral / total * 100
        if total > 0 else 0
    )

    # Sentiment KPI Cards

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Positive Reviews",
        f"{positive:,.0f}",
        f"{positive_percentage:.1f}%"
    )

    c2.metric(
        "Negative Reviews",
        f"{negative:,.0f}",
        f"{negative_percentage:.1f}%"
    )

    c3.metric(
        "Neutral Reviews",
        f"{neutral:,.0f}",
        f"{neutral_percentage:.1f}%"
    )

    st.divider()

    left, right = st.columns(2)

    # Sentiment Pie Chart

    with left:

        sentiment_data = pd.DataFrame({
            "Sentiment": [
                "Positive",
                "Negative",
                "Neutral"
            ],
            "Reviews": [
                positive,
                negative,
                neutral
            ]
        })

        fig = px.pie(
            sentiment_data,
            names="Sentiment",
            values="Reviews",
            hole=0.58,
            title="Overall Customer Sentiment",
            color="Sentiment",
            color_discrete_map=SENTIMENT_COLORS
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        st.plotly_chart(
            style_chart(fig),
            width="stretch"
        )

    # Sentiment Summary

    with right:

        st.subheader("Sentiment Overview")

        st.metric(
            "Total Analysed Reviews",
            f"{total:,.0f}"
        )

        st.metric(
            "Positive Sentiment",
            f"{positive_percentage:.1f}%"
        )

        st.metric(
            "Negative Sentiment",
            f"{negative_percentage:.1f}%"
        )

        st.caption(
            "Sentiment categories are generated using "
            "VADER's rule-based classification."
        )

    st.divider()

    # Restaurant-wise Sentiment

    st.subheader("Restaurant-wise Sentiment")

    sentiment_view = (
        df[
            [
                "Name",
                "Total_Reviews",
                "Positive_Percentage"
            ]
        ]
        .sort_values(
            "Positive_Percentage",
            ascending=False,
            na_position="last"
        )
        .rename(columns={
            "Positive_Percentage": "Positive Sentiment (%)"
        })
    )

    st.dataframe(
        sentiment_view,
        width="stretch",
        hide_index=True
    )


# 10. RESTAURANT CLUSTERING PAGE


elif page == "Restaurant Clustering":

    st.title("Restaurant Segmentation")

    st.caption(
        "Explore five restaurant groups identified "
        "using K-Means clustering."
    )

    # Cluster Summary

    cluster_summary = (
        df.groupby("Cluster")
        .agg(
            Restaurant_Count=("Name", "count"),
            Average_Cost=("Cost", "mean"),
            Average_Cuisines=("Cuisine_Count", "mean"),
            Average_Collections=("Collection_Count", "mean")
        )
        .reset_index()
        .round(2)
    )

    st.subheader("Cluster Profiles")

    st.dataframe(
        cluster_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # Cluster Visualization

    st.subheader("Restaurant Cluster Visualization")

    cluster_plot = df.copy()

    cluster_plot["Cluster_Label"] = (
        cluster_plot["Cluster"].astype(str)
    )

    fig = px.scatter(
        cluster_plot,
        x="Cost",
        y="Cuisine_Count",
        color="Cluster_Label",
        hover_name="Name",
        size="Collection_Count",
        size_max=25,
        title="K-Means Restaurant Segments",
        color_discrete_sequence=CHART_COLORS,
        labels={
            "Cost": "Average Cost (₹)",
            "Cuisine_Count": "Number of Cuisines",
            "Cluster_Label": "Cluster"
        }
    )

    st.plotly_chart(
        style_chart(fig),
        width="stretch"
    )

    st.divider()

    # Explore Individual Clusters

    st.subheader("Explore a Cluster")

    selected_cluster = st.selectbox(
        "Select Restaurant Cluster",
        sorted(
            df["Cluster"].dropna().unique()
        )
    )

    cluster_restaurants = df[
        df["Cluster"] == selected_cluster
    ]

    st.write(
        f"Restaurants in Cluster {int(selected_cluster)}: "
        f"**{len(cluster_restaurants)}**"
    )

    st.dataframe(
        cluster_restaurants[
            [
                "Name",
                "Cost",
                "Cuisine_Count",
                "Collection_Count"
            ]
        ],
        width="stretch",
        hide_index=True
    )


# 11. BUSINESS INSIGHTS PAGE


elif page == "Business Insights":

    st.title("Business Insights & Recommendations")

    st.caption(
        "Convert restaurant clustering and customer sentiment "
        "results into actionable business insights."
    )

    # Overall Business Metrics

    total_restaurants = df["Name"].nunique()

    average_cost = df["Cost"].mean()

    total_reviews = df["Total_Reviews"].sum()

    total_positive = df["Positive_Reviews"].sum()

    overall_positive = (
        total_positive / total_reviews * 100
        if total_reviews > 0 else 0
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Restaurants",
        f"{total_restaurants:,}"
    )

    col2.metric(
        "Average Restaurant Cost",
        f"₹{average_cost:,.0f}"
    )

    col3.metric(
        "Overall Positive Sentiment",
        f"{overall_positive:.1f}%"
    )

    st.divider()

    # Restaurant Segment Analysis

    st.subheader("Restaurant Segment Analysis")

    cluster_summary = (
        df.groupby("Cluster")
        .agg(
            Restaurant_Count=("Name", "count"),
            Average_Cost=("Cost", "mean"),
            Average_Cuisines=("Cuisine_Count", "mean"),
            Average_Collections=("Collection_Count", "mean")
        )
        .reset_index()
        .round(2)
    )

    largest_cluster = cluster_summary.loc[
        cluster_summary["Restaurant_Count"].idxmax()
    ]

    premium_cluster = cluster_summary.loc[
        cluster_summary["Average_Cost"].idxmax()
    ]

    col1, col2 = st.columns(2)

    col1.metric(
        "Largest Restaurant Segment",
        f"Cluster {int(largest_cluster['Cluster'])}",
        f"{int(largest_cluster['Restaurant_Count'])} restaurants"
    )

    col2.metric(
        "Highest Average Cost Segment",
        f"Cluster {int(premium_cluster['Cluster'])}",
        f"₹{premium_cluster['Average_Cost']:,.0f}"
    )

    st.dataframe(
        cluster_summary,
        width="stretch",
        hide_index=True
    )

    st.divider()

    # Customer Satisfaction Insights

    st.subheader("Customer Satisfaction Insights")

    eligible_restaurants = df[
        (df["Total_Reviews"] >= 10)
        & (df["Positive_Percentage"].notna())
    ]

    if not eligible_restaurants.empty:

        top_restaurant = eligible_restaurants.loc[
            eligible_restaurants["Positive_Percentage"].idxmax()
        ]

        st.metric(
            "Highest Positive Sentiment",
            str(top_restaurant["Name"]),
            f"{top_restaurant['Positive_Percentage']:.2f}% positive "
            f"({int(top_restaurant['Total_Reviews'])} reviews)"
        )

    else:

        st.info(
            "No restaurant has at least 10 reviews "
            "with available sentiment data."
        )

    st.divider()

    # Business Recommendations

    st.subheader("Business Recommendations")

    st.markdown("""
    **01 — Restaurant Segmentation**

    Use K-Means segments to understand different restaurant
    cost levels, cuisine diversity and collection patterns.

    **02 — Customer Experience**

    Monitor negative customer feedback to identify potential
    service and food-quality improvement areas.

    **03 — Market Positioning**

    Restaurants can compare their average cost and cuisine
    diversity with similar restaurants in their cluster.

    **04 — Customer Feedback Monitoring**

    Track sentiment percentages alongside review counts.
    Percentages based on very few reviews may not be reliable.
    """)


# END OF APPLICATION

