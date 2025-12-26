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

#new column
df = df.sort_values("observation_timestamp")

cryptos = st.multiselect("Cryptos",df["symbol"].unique(),default=["btc"])
metric = st.sidebar.radio("Métrique",["price_usd", "market_cap_usd", "volume_24h_usd", "circulating_supply"])

df_f = df[df["symbol"].isin(cryptos)]

#st.dataframe(df)
# Visualisation

##--------kPI------------------
latest = df_f.groupby("symbol").tail(1)

cols = st.columns(6)

for col, (_, row) in zip(cols, latest.iterrows()):
    col.metric(
        row["symbol"].upper(),
        f"{row['price_usd']:,.2f} $",
        f"{row['price_change_24h_percent']:.2f}%"
    )


# ----------trend per hour ----------
fig = px.line(
    df_f,
    x="observation_timestamp",
    y=metric,
    color="symbol",
    markers=True,
    title=f"Évolution de {metric}"
)
st.plotly_chart(fig, use_container_width=True)




####--------------cryptomonnaie market dominance------------------
df = df.groupby("name", as_index=False).first()

TOP_N = 9

top = df.nlargest(TOP_N, "market_cap_usd")
others_value = df["market_cap_usd"].sum() - top["market_cap_usd"].sum()

others = pd.DataFrame({
    "name": ["Others"],
    "market_cap_usd": [others_value]
})

df_pie = pd.concat([top, others])

fig = px.pie(
    df_pie,
    names="name",
    values="market_cap_usd",
    title="Market Cap Dominance"
)

st.plotly_chart(fig, use_container_width=True)

###-----------relationship price volume------------
fig = px.scatter(
    df,
    x="price_usd",
    y="volume_24h_usd",
    #size="market_cap_usd",
    color="name",
    hover_name="name",
    log_x=True,
    log_y=True,
    title="Price vs Volume (Log Scale)"
)

st.plotly_chart(fig, use_container_width=True)



