
import streamlit as st

def sql_query(conn, query: str):
    """
    Runs a SQL query and returns the result as a DataFrame.
    """
    st.code(query)
    st.dataframe(conn.query(query))