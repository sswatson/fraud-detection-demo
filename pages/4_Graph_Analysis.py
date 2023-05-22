
import streamlit as st
import pandas as pd
import io

from lib.snowpark import snowpark_graph

from lib.util import page_setup 

page_setup()

conn = st.experimental_connection('snowpark')

"""
# Graph Analysis

## Graph Features

With the graph features having been computed as shown in the previous section, we can now observe how they improve model performance:
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
For comparison, here are the results from the previous section:
"""

st.dataframe(
    pd.read_csv(
        io.StringIO(
            """
Metric	Value
Precision	0.9029126214
Recall	0.7246753247
AUC	0.9251578768
Accuracy	0.8887070376
F1 Score	0.8040345821
"""
        ),
        sep="\t",
    )
)

"""
*Note 1: we'll have to iterate on this a bit. The improvement is marginal, and the precision got worse.*

*Note 2: we'll also want to look at feature importance*.
"""