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
st.caption("Data from coingecko API – pipeline Airflow")


# Sidebar
st.sidebar.markdown("<h4>Measure</h4>", unsafe_allow_html=True)


#st.checkbox("BTC", "ETH", "SOL")
#st.button("Lancer")

#extraction
conn = sqlite3.connect("/home/lieums/airflow_project/pluto_database.db")
query = """SELECT * FROM crypto_market"""
df = pd.read_sql_query(query, conn)
df['price_usd'] = pd.to_numeric(df['price_usd'])
df['market_cap_usd'] = pd.to_numeric(df['market_cap_usd'])
df['volume_24h_usd'] = pd.to_numeric(df['volume_24h_usd'])


#st.dataframe(df)
# Visualisation

###---------VOLATILITE-------------
vol = (df.groupby("symbol")["price_change_24h_percent"].std().reset_index())
vol = vol.sort_values("price_change_24h_percent", ascending=False)
top_n = st.slider("Choisir le nombre", 3, 20, 10)
most_vol = vol.head(top_n)
less_vol = vol.tail(top_n)

fig = px.bar(
    most_vol,
    x="symbol",
    y="price_change_24h_percent",
    color='symbol',
    title="Cryptomonnaies les plus volatiles (std des variations 24h)"
)

st.plotly_chart(fig)

##------------------------------------------
fig = px.bar(
    less_vol,
    x="symbol",
    y="price_change_24h_percent",
    color='symbol',
    title="Cryptomonnaies les moins volatiles (std des variations 24h)"
)

st.plotly_chart(fig)

