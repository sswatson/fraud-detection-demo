import streamlit as st
import pandas as pd
import io

from lib.snowpark import snowpark_simple
from lib.queries import simple_feature_query

from lib.util import page_setup, next_page
from lib.sql import sql_query

page_setup()

conn = st.experimental_connection("snowpark")

"""
# Simple Features

## Computing the Features in Snowflake

Calculating features in a cloud-native system like Snowflake provides scalability and performance advantages relative to conventional in-memory solutions, so we will show how to build a table of summary features using a Snowflake SQL query.

As a starting point, let's build a machine learning model using simple summary statistics from the `voc`, `sms`, and `app` tables. We will use the following features:

- **outgoing_call_count**: The number of calls placed by the user.

- **incoming_call_count**: The number of calls received by the user.

- **outgoing_text_count**: The number of phone numbers to which a user has made voice calls.

- **incoming_text_count**: The number of phone numbers from which a user has received voice calls.

- **callbacks**: The number of phone numbers that a user has both received a voice call from and later called back.

- **textbacks**: The number of phone numbers that a user has both received a text message from and later texted back.

These features are all simple enough that we can calculate them relatively easily in SQL. The query below (collapsed because it is quite long!) materializes a feature table:
"""

with st.expander("View SQL query for simple features:"):
    st.code(simple_feature_query)

"""
Here's what the first few rows look like:
"""

sql_query(conn, "SELECT * FROM simple_features LIMIT 5;")

"""
## Predicting Fraud

### Training the Model

Let's train a baseline machine learning model using the features computed above. We can do this using *Snowpark*, which provides Python support inside Snowflake:
"""

with st.expander("View Snowpark Python machine-learning code:"):
    st.code(snowpark_simple, "python")

"""
### Model Results

The results of the model on the test set are as shown:
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

next_page("Snowflake-RAI Integration")
