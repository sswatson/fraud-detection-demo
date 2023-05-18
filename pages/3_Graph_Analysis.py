
import streamlit as st
import pandas as pd
import io

from lib.snowpark import snowpark_graph
from lib.dataframe_graph import dataframe_graph
from streamlit_extras.switch_page_button import switch_page

from lib.util import set_page_config, sql_query
set_page_config()

conn = st.experimental_connection('snowpark')

"""
# Graph Analysis

While the simple features computed on the previous page are a helpful starting point, the graph structure of the connection network provides a rich source of information that we can use to improve our model.

## Graph Visualization

To better appreciate the graph structure of the data, let's look at some graph visualizations:
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

"""
## Graph Features

The simple features in the previous section are *local* quantities from the graph point of view. For example, a user's callback count can be computed from information about the user's calls with their neighors in the graph.

However, often in fraud detection the key information that you want to make available to the machine learning model pertains to non-local structure. Examples of non-local graph structure include:

- The size of a node's connected component. This is the number of nodes that are reachable from the node by following edges.
- Each node's *PageRank* score. This is the probability that a long-running random walk on the graph will end up at the node.
- The *Eigenvector Centrality* of each node. This is a measure of how well-connected a node is to other well-connected nodes.

Because of the complex algorithms required to compute these quantities, computing them in plain SQL is very difficult. Therefore, developers usually use an external graph library for this purpose. While there are several graph analytics technologies, RelationalAI offers some unique benefits:
1. Seamless integration with Snowflake. You can use the same SQL query to compute graph features as you would use to compute simple features.
2. Cloud-native architecture. This means that you can use RelationalAI on datasets that are too large to fit on a single node.

In the next section, we'll look at how to compute these graph features using RelationalAI. In the meantime, let's look at how the model's performance improves when we have these quantities available:
"""

with st.expander("View SQL query for graph features:"):
    st.code(snowpark_graph)

st.dataframe(pd.read_csv(io.StringIO(
"""
Metric	Value
Precision	0.8780487805
Recall	0.7659574468
AUC	0.9224946494
Accuracy	0.8951678952
F1 Score	0.8181818182
"""
), sep="\t"))

"""
*Note 1: we'll have to iterate on this a bit. The improvement is marginal, and the precision got worse.*

*Note 2: we'll also want to look at feature importance*.
"""

if st.button("Snowflake-RAI Integration→"):
    switch_page("Snowflake-RAI Integration")