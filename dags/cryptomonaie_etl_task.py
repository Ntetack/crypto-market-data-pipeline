import requests
import pandas as pd 
import sqlite3, uuid
from datetime import datetime


##-------------------------------extract and store in staging area---------------------------
def create_tables():
    conn = sqlite3.connect('pluto_database.db')
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto_staging (
        staging_id INTEGER PRIMARY KEY AUTOINCREMENT,

        id TEXT,
        symbol TEXT,
        name TEXT,
        image TEXT,
        current_price REAL,
        market_cap REAL,
        market_cap_rank INTEGER,
        fully_diluted_valuation REAL,
        total_volume REAL,
        high_24h REAL,
        low_24h REAL,
        price_change_24h REAL,
        price_change_percentage_24h REAL,
        market_cap_change_24h REAL,
        market_cap_change_percentage_24h REAL,
        circulating_supply REAL,
        total_supply REAL,
        max_supply REAL,
        ath REAL,
        ath_change_percentage REAL,
        ath_date TEXT,
        atl REAL,
        atl_change_percentage REAL,
        atl_date TEXT,
        roi REAL,
        roi_times REAL,
        roi_currency TEXT,
        roi_percentage REAL,
        last_updated TEXT,

        -- champs techniques
        ingestion_timestamp TIMESTAMP,
        batch_id TEXT,
        processed INTEGER DEFAULT 0
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS crypto_market (
        pk_id INTEGER PRIMARY KEY AUTOINCREMENT,

        id TEXT,
        symbol TEXT,
        name TEXT,

        price_usd REAL,
        market_cap_usd REAL,
        volume_24h_usd REAL,

        circulating_supply REAL,
        total_supply REAL,
        max_supply REAL,

        price_change_24h REAL,
        price_change_24h_percent REAL,
        market_cap_change_24h REAL,

        market_cap_rank INTEGER,

        observation_timestamp TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()


##-----------------extract data------------------------------------------
def extract_data(**context):
    from datetime import timezone
    import uuid

    execution_ts = context["logical_date"].astimezone(timezone.utc)

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': 'false'
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("Erreur API CoinGecko")

    df = pd.json_normalize(response.json())

    # champs techniques
    df['ingestion_timestamp'] = execution_ts
    df['batch_id'] = str(uuid.uuid4())
    df['processed'] = 0

    conn = sqlite3.connect('pluto_database.db')
    df.to_sql('crypto_staging', conn, if_exists='append', index=False)
    conn.close()



###----------------------------data transformation--------------------------
def transform_load_data():
    conn = sqlite3.connect('pluto_database.db')

    df = pd.read_sql("""
        SELECT *
        FROM crypto_staging
        WHERE processed = 0
    """, conn)

    if df.empty:
        conn.close()
        return

    df_curated = df[[
        'id','symbol','name','current_price','market_cap','total_volume',
        'circulating_supply','total_supply','max_supply',
        'price_change_24h','price_change_percentage_24h',
        'market_cap_change_24h','market_cap_rank',
        'last_updated'
    ]].copy()

    df_curated.columns = [
        'id','symbol','name','price_usd','market_cap_usd','volume_24h_usd',
        'circulating_supply','total_supply','max_supply',
        'price_change_24h','price_change_24h_percent',
        'market_cap_change_24h','market_cap_rank',
        'observation_timestamp'
    ]

    df_curated['observation_timestamp'] = pd.to_datetime(
        df_curated['observation_timestamp'], utc=True
    )

    df_curated.to_sql('crypto_market', conn, if_exists='append', index=False)

    conn.execute("""
        UPDATE crypto_staging
        SET processed = 1
        WHERE processed = 0
    """)

    conn.commit()
    conn.close()
