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
st.set_page_config(page_title="Drug Performance Explorer", layout="wide")
st.title("💊 Drug Performance Evaluation App")
st.markdown("Analyze and explore drug performance across disease classes and conditions.")

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔧 Filters")

# Performance type toggle
performance_type = st.sidebar.radio("Performance type", ["Average", "Weighted"])
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
    filtered_df.groupby(['d]()_
