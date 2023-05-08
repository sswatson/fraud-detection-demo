import streamlit as st
from lib.sql_query import sql_query

st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon="❄️",
)

"""
## RelationalAI Fraud Detection Demo

The goal of this project is to detect spam using app usage records, text message data, and voice call data in China from August 2019 to March 2020. The dataset we will use contains *real*, anonymized telecommunications data that was released by China Mobile Sichuan Corporation.

The dataset includes four tables (plus a `column_descriptions` table):
"""

conn = st.experimental_connection('snowpark')

sql_query(conn, """SELECT * FROM voc LIMIT 5;""")
