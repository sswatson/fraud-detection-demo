
import streamlit as st

from lib.util import page_setup, next_page
from lib.dataframe_graph import dataframe_graph

page_setup()

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
    SUBSTR(PHONE_NO_M, 1, 8) as USER_ID,
    CASE WHEN LABEL = 0 THEN 'no' else 'yes' END AS FRAUDSTER,
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
Therefore, training an effective model will require us to extract features about each user from the call, text, and app usage tables. Here's what the call table looks like, for example:
"""

st.code("SELECT * FROM voc LIMIT 10;", "sql")

df = conn.query(f"""
SELECT
    SUBSTR(PHONE_NO_M, 1, 8) as USER_ID,
    SUBSTR(OPPOSITE_NO_M, 1, 8) as CALL_PARTNER,
    CASE WHEN CALLTYPE_ID = 1 THEN 'incoming' ELSE 'outgoing' END AS CALL_TYPE,
    START_DATETIME AS TIME,
    CALL_DUR AS DURATION
FROM
    voc
LIMIT 10;
""")

df

"""
## Graph Visualization

Given the network structure of this dataset, it's helpful to visualize the relationships between users as a graph. For example, the figure below shows calls between a `USER_ID` and a `CALL_PARTNER` as directed edge from the former to the latter:

*Note: We can replace this visualization with a static image at a later stage.*
"""

first_graph_query = """
WITH USER_SUBSET AS (
    SELECT DISTINCT phone_no_m FROM user LIMIT 10
)
SELECT DISTINCT
    phone_no_m AS source,
    opposite_no_m AS target
FROM voc
WHERE phone_no_m IN (SELECT phone_no_m FROM USER_SUBSET)
ORDER BY opposite_no_m
LIMIT 1000;
"""

pretty_query = """
WITH USER_SUBSET AS (
    SELECT DISTINCT user_id FROM user LIMIT 10
)
SELECT DISTINCT
    user_id AS source,
    call_partner AS target
FROM voc
WHERE user_id IN (SELECT user_id FROM USER_SUBSET)
LIMIT 1000;
"""

with st.expander("View SQL query for graph visualization:"):
    st.code(pretty_query)

df = conn.query(first_graph_query)
dataframe_graph(df)

"""
This visualization shows that the phone connection exhibit clustering behavior, with relatively sparse connectivity between clusters. This has to do with the way the data were compiled: the featured users (those in the first column of `voc`) are at the centers of the clusters, and the nodes around them represent other network users who are included in the dataset because of their connections to the featured users.

Looking at this graph, you can think of several features that may be useful for distinguishing fraud users from non-fraud users. For example, fraudsters may be more likely to call other fraudsters, or to call numbers outside of their network.

In the next section, we'll take a look at how to compute several such features with SQL.
"""

next_page("Simple Features")