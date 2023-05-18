
import streamlit as st

from lib.util import set_page_config, check_password
from streamlit_extras.switch_page_button import switch_page

set_page_config()

if check_password():
    """
    # Fraud Detection with Snowflake and RelationalAI

    *NOTE: THIS CONTENT IS WORK-IN-PROGRESS*

    In an increasingly digital world, the menace of fraud has grown exponentially, leading to significant financial losses and numerous other non-monetary impacts. In 2021, the total global loss due to fraud was approximately $40 billion.

    In November 2022, people in the U.S. received over 47 billion spam texts. Beyond the considerable financial losses, fraud also results in a number of other significant impacts. Victims often experience great dissatisfaction, a sense of violation, and loss of trust in institutions. They may also lose substantial time in efforts to resolve the fraudulent issues. The increasing need for solutions is clear.

    This app will explain how telecommunications companies can leverage cloud database technologies like Snowflake and RelationalAI to identify fraudulent actors.
    """

    if st.button("The Dataset →"):
        switch_page("The Dataset")