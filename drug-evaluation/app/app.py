import streamlit as st
import pandas as pd
import os

# -------------------------------
# Load Data Safely
# -------------------------------
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, "..", "data", "df_clean.csv")
df_clean = pd.read_csv(csv_path)
df_streamlit = df_clean.copy()

# -------------------------------
# Streamlit Config
# -------------------------------
# Streamlit config
st.set_page_config(page_title="Drug Performance Explorer", layout="wide")

# Disclaimer warning (high visibility)
st.warning(
    "⚠️ **Disclaimer:** This app is for informational purposes only. "
    "It does not provide medical advice, diagnosis, or treatment. "
    "Always consult a licensed healthcare professional before making any medical decisions."
)

# App title and intro
st.title("💊 Drug Performance Evaluation App")
st.markdown("Analyze and explore drug performance across disease classes and conditions.")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔧 Filters")

# Performance type toggle
performance_type = st.sidebar.radio("Performance type", ["Average", "Weighted"])

if performance_type == "Average":
    st.sidebar.markdown(
        "<span style='color:red;'>📊 Average = Equal weight of effectiveness, ease of use, and satisfaction.</span>",
        unsafe_allow_html=True
    )
else:
    st.sidebar.markdown(
        "<span style='color:red;'>📈 Weighted = Same metrics, but prioritizes effectiveness more.</span>",
        unsafe_allow_html=True
    )

perf_column = "performance" if performance_type == "Average" else "weighted_performance"

# Disease class selector
disease_class = st.sidebar.selectbox(
    "Select disease class",
    sorted(df_streamlit['disease_class'].dropna().unique())
)

# Minimum review count
min_reviews = st.sidebar.slider(
    "Minimum review count",
    min_value=0,
    max_value=int(df_streamlit['reviews'].max()),
    value=50
)

# Filtered data
filtered_df = df_streamlit[
    (df_streamlit['disease_class'] == disease_class) &
    (df_streamlit['reviews'] >= min_reviews)
].copy()

# -------------------------------
# Section 1: Top Drugs by Disease Class
# -------------------------------
st.subheader(f"🏆 Top Drugs in '{disease_class}' (Sorted by {performance_type} Performance)")

top_df = (
    filtered_df.groupby(['drug', 'condition'], as_index=False)
    .agg(avg_performance=(perf_column, 'mean'), reviews=('reviews', 'sum'))
    .sort_values(by='avg_performance', ascending=False)
    .head(10)
)

# Display table
st.dataframe(top_df)

# Display Streamlit-native bar chart
if not top_df.empty:
    top_df_display = top_df.copy()
    top_df_display['drug_condition'] = top_df_display['drug'] + ' (' + top_df_display['condition'] + ')'
    top_df_display = top_df_display.set_index('drug_condition')
    st.bar_chart(top_df_display['avg_performance'])
else:
    st.warning("No data available for this combination.")

# -------------------------------
# Section 2: Recommend Drugs by Condition
# -------------------------------
st.subheader("🔍 Recommend Drugs by Condition")

user_condition = st.text_input("Enter a condition (e.g., 'Diabetes', 'Back Pain')")

# Drug type filter
drug_types = df_streamlit['type'].unique()
selected_types = st.multiselect("Filter by Drug Type", drug_types, default=list(drug_types))

if user_condition:
    cond_filtered = df_streamlit[
        (df_streamlit['condition'].str.contains(user_condition, case=False, na=False)) &
        (df_streamlit['type'].isin(selected_types))
    ]

    if not cond_filtered.empty:
        recommendations = (
            cond_filtered.groupby('drug', as_index=False)
            .agg(avg_performance=(perf_column, 'mean'), reviews=('reviews', 'sum'))
            .sort_values(by='avg_performance', ascending=False)
            .head(10)
        )
        st.success(f"Top drug recommendations for **{user_condition}**:")
        st.dataframe(recommendations)
    else:
        st.warning("No matching condition found with the selected drug types.")




