import streamlit as st
import polars as pl
from datetime import datetime
import plotly.express as px
import pandas as pd

# Set page config
st.set_page_config(
    page_title="Berghain Analysis",
    page_icon="🎧",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return pl.read_parquet("prueba_parquet.parquet")

df = load_data()
pdf = df.to_pandas()

# Title with factory icon
st.title("🏭 Berghain Club Analysis")  # Added factory icon to the main page title
st.write("Explore events and artists at Berghain from 2010 onwards")

# Sidebar content
st.sidebar.header("Year Picker Context")
st.sidebar.write("""
This application provides an interactive analysis of events and performances at the Berghain club. 
You can explore the data by selecting different years to see how the number of events and artist performances have changed over time.
""")
st.sidebar.markdown("[Created by alejofig.com](https://alejofig.com)")

min_year = datetime.strptime(df["date"].min(), "%Y-%m-%d").year
max_year = datetime.strptime(df["date"].max(), "%Y-%m-%d").year

# Add "All Data" option to the year picker
year_options = ["All Data"] + list(range(min_year, max_year + 1))

selected_year = st.sidebar.selectbox(
    "Select Year",
    options=year_options,
    index=0
)

# Filter data based on selected year
if selected_year == "All Data":
    filtered_df = df
else:
    filtered_df = df.filter((pl.col("date").str.slice(0, 4) == str(selected_year)))

# Example analysis: Count performances by artist
artist_counts = (
    filtered_df
    .group_by("artist")
    .agg(pl.count("artist").alias("count"))
    .sort("count", descending=True)
)
st.write("Artist Performance Counts:")
st.dataframe(artist_counts.to_pandas())

# Example analysis: Events over time
events_over_time = (
    filtered_df
    .group_by("date")
    .agg(pl.count("date").alias("count"))
    .sort("date")
)
fig = px.line(events_over_time.to_pandas(), x='date', y='count', title='Events Over Time')
st.plotly_chart(fig)

# Display filtered data
st.write("Filtered Events Data:")
st.dataframe(filtered_df.to_pandas())