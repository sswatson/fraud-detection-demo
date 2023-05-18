
import streamlit as st

from streamlit.connections import SnowparkConnection
import pandas as pd

def set_page_config():
    st.set_page_config(
        page_title="Fraud Detection Demo",
        page_icon="❄️",
    )

import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


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
