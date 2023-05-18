
import streamlit as st

from lib.util import set_page_config
from streamlit_extras.switch_page_button import switch_page
set_page_config()

conn = st.experimental_connection('snowpark')

"""
# The Dataset

We will use a dataset released in 2022 by the Chinese telecommuniations company *Sichuan Mobile*. This dataset is notable because it the data is not simulated; instead, it is drawn from real-world usage on the Sichuan Mobile network.

Our goal will be to build a machine learning model to predict whether a user is a fraudster based on their usage of the network.

## Overview

The dataset consists of four tables: `user`, `voc`, `sms`, and `app`. The first table contains about 6,000 rows, one for each user featured in the dataset. The other three tables contain a few million rows each, as they contain one for each call, text, and app usage event to involving each featured user.

The `user` table contains limited information for predicting the fraudster status of each user:
"""

st.code(
    f"""SELECT * FROM user LIMIT 5;""",
    "sql"
)

df = conn.query(f"""
SELECT
    SUBSTR(PHONE_NO_M, 1, 5) || '...' as USER_ID,
    LABEL AS FRAUDSTER,
    CITY_NAME,
    COUNTY_NAME,
    ARPU201908 AS BILL_AUG_2019,
    ARPU201909 AS BILL_SEP_2019,
    ARPU201910 AS BILL_OCT_2019,
    ARPU201911 AS BILL_NOV_2019,
    ARPU201912 AS BILL_DEC_2019,
    ARPU202001 AS BILL_JAN_2020,
    ARPU202002 AS BILL_FEB_2020,
    ARPU202003 AS BILL_MAR_2020
FROM
user
LIMIT 5;
""")
                
df

"""
Therefore, training an effective model will require us to extract features about each user from the call, text, and app usage tables. Doing this in Snowflake provides scalability and performance advantages relative to conventional in-memory solutions, so we will show how to build a table of summary features using a Snowflake SQL query.
"""

if st.button("Simple Features →"):
    switch_page("Simple Features")