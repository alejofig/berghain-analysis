import streamlit as st
import polars as pl
import plotly.express as px

# Configurar la página
st.set_page_config(
    page_title="Berghain Analysis",
    page_icon="🎧",
    layout="wide"
)

# Cargar datos con lazy evaluation
@st.cache_data
def load_data():
    return pl.scan_parquet("prueba_parquet.parquet").select(["date", "artist"])

df = load_data().with_columns([pl.col("date").str.strptime(pl.Date, "%Y-%m-%d")])

# Sidebar
st.sidebar.header("Year Picker Context")
st.sidebar.write("""
Esta aplicación proporciona un análisis interactivo de eventos y actuaciones en Berghain.
Selecciona un año para ver cómo han cambiado los eventos y artistas a lo largo del tiempo.
""")
st.sidebar.write("Creado por alejofig.com")

# Agrupación de datos optimizada
artist_counts = (
    df
    .group_by("artist")
    .agg(pl.count("artist").alias("count"))
    .sort("count", descending=True)
    .collect()
)
st.write("Conteo de Actuaciones por Artista:")
st.dataframe(artist_counts.to_pandas())

# Análisis de eventos a lo largo del tiempo
events_over_time = (
    df
    .group_by("date")
    .agg(pl.count("date").alias("count"))
    .sort("date")
    .collect()
)
fig = px.line(events_over_time.to_pandas(), x='date', y='count', title='Eventos a lo Largo del Tiempo')
st.plotly_chart(fig)

# Mostrar datos filtrados
st.write("Datos Filtrados de Eventos:")
st.dataframe(df.collect().to_pandas())
