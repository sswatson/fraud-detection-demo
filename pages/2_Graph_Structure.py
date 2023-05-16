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

## Primary Users

The users in the `phone_no_m` column of the call-records table (`voc`) are all in the `users` table:
"""

sql_query(conn, f"""
SELECT phone_no_m FROM voc
EXCEPT
SELECT phone_no_m FROM user;
""")
          
"""
However, there are many more users in the `opposite_no_m` column of the `voc` table than in the `users` table:
"""

sql_query(conn, f"""
SELECT COUNT(DISTINCT opposite_no_m) FROM voc
""")

"""
This suggests that the dataset was constructed by choosing a subset of users — let's call them *primary users* — and collecting all of their call records, including calls to and from people who are not primary users.

## Graph Visualizations

We can visualize the structure of the network of calls in the dataset as a graph, with nodes being individuals and edges being calls between them. To get a manageable dataset to render, we'll select a small number of distinct primary users from the dataset and find everyone they called or received calls from:
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
LIMIT 1000;
"""

st.code(first_graph_query)

df = conn.query(first_graph_query)
dataframe_graph(df)

"""
This graph gives the impression that the graph consists of clusters of users, with a relatively low density of edges establishing a connection between clusters.

This observation suggests a different graph that will help us better understand the structure of this dataset: the graph whose nodes are primary users and whose edges tell us whether two primary users have a common contact. In other words, the graph whose nodes are the *clusters* in the figure above:
"""

second_graph_query = """
WITH user_subset AS (
    SELECT DISTINCT phone_no_m FROM user LIMIT 50
)
SELECT DISTINCT
    v1.phone_no_m AS source,
    v2.phone_no_m AS target
FROM voc v1
JOIN voc v2
    ON v1.opposite_no_m = v2.opposite_no_m
    AND v1.phone_no_m != v2.phone_no_m
    AND v1.phone_no_m IN (SELECT phone_no_m FROM USER_SUBSET)
    AND v2.phone_no_m IN (SELECT phone_no_m FROM USER_SUBSET)
"""

st.code(second_graph_query)

df = conn.query(second_graph_query)

dataframe_graph(df)

"""
We can see that this graph is actually pretty densely connected!

We can calculate how densely connected it is by computing the probability that two randomly chosen users have an edge between them (this time for the entire dataset, not just a subset):
"""

sql_query(conn, f"""
WITH edge_counts AS (
    SELECT
        COUNT(DISTINCT v1.phone_no_m, v2.phone_no_m) AS num_edges,
        COUNT(DISTINCT v1.phone_no_m) AS n
    FROM voc v1
    JOIN voc v2
        ON v1.opposite_no_m = v2.opposite_no_m
        AND v1.phone_no_m != v2.phone_no_m
)
SELECT
    num_edges,
    n * (n-1) AS num_possible_edges,
    num_edges * 1.0 / num_possible_edges AS edge_probability
FROM edge_counts;
""")
          
"""
With about 29% of pairs being connected by a common contact, this graph is indeed quite well-connected. 
"""


if st.button("Feature Engineering →"):
    switch_page("Feature Engineering")