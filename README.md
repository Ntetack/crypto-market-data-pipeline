# crypto-market-data-pipeline
crypto market data pipeline with airflow and streamlit
Crypto Market Data Pipeline

# Présentation du projet

Ce projet met en place un système complet de collecte, stockage, transformation et visualisation de données de crypto-monnaies, basé sur l’API publique de CoinGecko.

Il s’agit d’un pipeline de données de type ETL (Extract – Transform – Load) orchestré avec Apache Airflow, stockant les données dans SQLite, puis exposant des visualisations interactives via Streamlit.

# Architecture
CoinGecko API ---> [ Extraction ] ---> [ Staging SQLite ] ---> [ Transformation ] ---> [ Final data ] ---> [ Streamlit Dashboard ]


# Objectifs

Collecter périodiquement les données du marché crypto

Conserver l’intégralité des données sources sans perte

Permettre l’historisation et la reprise après échec

Produire des tables propres pour l’analyse

Visualiser les indicateurs clés du marché

# Technologies utilisées

- Python

- Apache Airflow 3.0

- SQLite

- Pandas

- Streamlit

- CoinGecko API
  
- Plotly
