
import streamlit as st

from lib.sql import sql_query
conn = st.experimental_connection("snowpark")

"""
# Example input components
"""

selected_table = st.selectbox("Table", ["user", "app", "sms", "voc"])

selected_limit = st.selectbox("Limit", [5, 10, 15])

st.write("You selected:", selected_table)

sql_query(conn, f"SELECT * FROM {selected_table} LIMIT {selected_limit};")