import streamlit as st

from lib.dataframe_graph import dataframe_graph
from lib.util import page_setup, next_page

page_setup()

conn = st.experimental_connection("snowpark")

"""
While the simple features are a helpful starting point, the graph structure of the connection network provides a rich source of information that we can use to improve our model predictions.

## Graph Visualization

To better understand the structure in the dataset, let's look at some graph visualizations:
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

with st.expander("View SQL query for graph visualization:"):
    st.code(first_graph_query)

df = conn.query(first_graph_query)
dataframe_graph(df)

"""
This visualization shows that the phone connection exhibit clustering behavior, with relatively sparse connectivity between clusters. This has to do with the way the data were compiled: the featured users are at the centers of the clusters, and the nodes around them represent non-featured users who are included in the dataset because of their connections to the featured users.

This visualization suggests looking at another graph: the graph whose nodes represent the clusters in the above visualization. In other words, we will create a graph where the nodes are featured users and two nodes are connected if they have a common phone call contact.
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

with st.expander("View SQL query for graph visualization:"):
    st.code(second_graph_query)

df = conn.query(second_graph_query)

dataframe_graph(df)

"""
Since this graph has a large, quite densely connected component, we can see that the connectivity structure of the original network is actually quite rich: locally it consists of sparsely connected clusters, but globally these clusters link up through common contacts.
"""

next_page("Snowflake-RAI Integration")