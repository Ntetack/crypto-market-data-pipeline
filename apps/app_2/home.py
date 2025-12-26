import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import unidecode
import sqlite3


# CSS
css_file = "styles/template1_style.css"
with open(css_file) as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(page_title="Crypto Dashboard", layout="wide")

st.title("Crypto Monitoring Dashboard")
st.caption("Sample data from coingecko API – pipeline Airflow")


# Sidebar
st.sidebar.markdown("<h4>Measure</h4>", unsafe_allow_html=True)


#st.checkbox("BTC", "ETH", "SOL")
#st.button("Lancer")

#extraction
conn = sqlite3.connect("/home/lieums/airflow_project/pluto_database.db")
query = """SELECT * FROM crypto_market"""
df = pd.read_sql_query(query, conn)
st.dataframe(df.sample(200))
