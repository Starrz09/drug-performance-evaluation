# -------------------------------
# Section 3: High Performance but Low Review Count
# -------------------------------
st.subheader("🌟 High Performance but Low Review Count")

high_perf = df_streamlit[
    (df_streamlit['performance'] >= 4.5) &
    (df_streamlit['reviews'] <= 5)
]

high_perf_display = high_perf[['drug', 'condition', 'performance', 'reviews']].drop_duplicates()
st.dataframe(high_perf_display.sort_values(by='performance', ascending=False).head(10))
