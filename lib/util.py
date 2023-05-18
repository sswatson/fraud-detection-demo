
import streamlit as st

from streamlit.connections import SnowparkConnection
import pandas as pd

def set_page_config():
    st.set_page_config(
        page_title="Fraud Detection Demo",
        page_icon="❄️",
    )

def sql_query(conn: SnowparkConnection, query: str):
    """
    Runs a SQL query and returns the result as a DataFrame.
    """
    st.code(query, language="sql")
    st.dataframe(truncate_strings(conn.query(query)))

def truncate_strings(df: pd.DataFrame):
    df = df.copy()  # To avoid modifying the original dataframe
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x[:8] + "..." if isinstance(x, str) and len(x) > 15 else x
        )
    return df
