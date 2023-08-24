
import streamlit as st

from streamlit_extras.switch_page_button import switch_page

def next_page(name: str):
    btn = st.button(name + " →")
    if btn:
        switch_page(name)

def page_setup():
    print("Rendering page")
    st.set_page_config(
        page_title="Fraud Detection Demo",
        page_icon="❄️",
    )
    if not check_password():
        st.stop()

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