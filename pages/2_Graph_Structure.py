import streamlit as st

from lib.dataframe_graph import dataframe_graph

from streamlit_extras.switch_page_button import switch_page

from streamlit_agraph import agraph, Node, Edge, Config

from streamlit_extras.switch_page_button import switch_page

from lib.sql_query import sql_query

st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon="❄️",
)

conn = st.experimental_connection("snowpark")

"""
# Graph Structure

One notable characteristic of this dataset is that much of the predictive value available in the dataset comes from the network structure of the data.

In other words, we don't have a lot of personal user attributes, but we do have a lot of information about who they communicate with, who those people communicate with, and so on.

For this reason, it's helpful to visualize the data as a graph whose nodes are users and whose edges are communications between users.
"""

offset = st.number_input("user number", 0, 1000, 100)

df = conn.query(
f"""
WITH random_user AS (
    SELECT phone_no_m FROM user ORDER BY phone_no_m LIMIT 1 OFFSET {offset}
), other_users AS (
    SELECT DISTINCT opposite_no_m AS phone_no
    FROM voc
    WHERE phone_no_m = (SELECT phone_no_m FROM random_user)
    LIMIT 100
), all_users AS (
    SELECT phone_no_m AS phone_no FROM random_user
    UNION ALL
    SELECT phone_no FROM other_users
)
SELECT 
    v.phone_no_m, v.opposite_no_m
FROM voc v
JOIN all_users u1 ON v.phone_no_m = u1.phone_no
JOIN all_users u2 ON v.opposite_no_m = u2.phone_no;
"""
)

dataframe_graph(df)
