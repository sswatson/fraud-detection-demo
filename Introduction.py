import streamlit as st

from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon="❄️",
)

"""
# RelationalAI Fraud Detection Demo

## Introduction

In this web app, we'll show how you can use Snowflake and RelationalAI to detect fraud using app usage records, text message data, and voice call data in China from August 2019 to March 2020.

The dataset we will use is notable because it contains *real*, anonymized telecommunications data that was released by China Mobile Sichuan Corporation.
"""

if st.button("Get started →"):
    switch_page("The Data")