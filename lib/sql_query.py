import streamlit as st
from streamlit.connections import SnowparkConnection

def sql_query(conn: SnowparkConnection, query: str):
    """
    Runs a SQL query and returns the result as a DataFrame.
    """
    st.code(query, language="sql")
    st.dataframe(conn.query(query))
