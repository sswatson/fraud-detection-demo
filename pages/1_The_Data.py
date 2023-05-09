
import streamlit as st
import io
import pandas as pd
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Fraud Detection Demo",
    page_icon="❄️",
)

from lib.sql_query import sql_query

conn = st.experimental_connection('snowpark')

"""
# The Data

## Overview

The dataset we will use contains four tables: `voc`, `sms`, `app`, and `user`. The dataset can be accessed via Baidu's *AI Studio* [here](https://aistudio.baidu.com/aistudio/datasetdetail/40690/) under a CC0 license. You can find an academic article describing the dataset [here](https://doi.org/10.1016/j.future.2022.07.020).

Use the dropdown menu below to select a table. Your selection will update the SQL query, and the new query will be run against the Snowflake database containing the data we're using:
"""

table_name = st.selectbox("table name:", ["voc", "sms", "app", "user"])

sql_query(conn, f"""SELECT * FROM {table_name} LIMIT 5;""")

"""
Some of the column names are difficult to interpret on their own, so here are some descriptions:
"""

st.dataframe(pd.read_csv(io.StringIO("""
Table	Column	Description
app	phone_no_m	account phone number identifier
app	busi_name	name of the application used
app	flow	bandwidth used by the application on the given phone in the given month
app	month_id	month in which the application was used
sms	phone_no_m	account phone number identifier
sms	opposite_no_m	peer phone number
sms	calltype_id	downlink (1) or uplink (2)
sms	request_datetime	time when sms was sent
users	phone_no_m	account phone number identifier
users	city_name	subscriber's city of residence
users	county_name	subscriber's county of residence
users	idcard_cnt	number of SIM cards on the account
users	arpu_201908	account's billing amount in Aug 2019
users	arpu_201909	account's billing amount in Sep 2019
users	arpu_201910	account's billing amount in Oct 2019
users	arpu_201911	account's billing amount in Nov 2019
users	arpu_201912	account's billing amount in Dec 2019
users	arpu_202001	account's billing amount in Jan 2020
users	arpu_202002	account's billing amount in Feb 2020
users	arpu_202003	account's billing amount in Mar 2020
users	label	whether the user is a spammer (1) or not (0)
voc	phone_no_m	account phone number identifier
voc	opposite_no_m	peer phone number
voc	calltype_id	incoming (1) or outgoing (2) or neither (3)
voc	start_datetime	starting time of the phone call
voc	call_dur	duration of the phone call
voc	city_name	name of the city of the peer phone number
voc	county_name	name of the county of the peer phone number
voc	imei_m	phone's device identifier
"""), sep="\t"))

"""
Most notably, the `label` column in the `user` table indicates whether the user is a spammer (1) or not (0). This is the column we'll be trying to predict.
"""

"""
## Summary Statistics
"""

"""
Let's take a look at the number of rows in each table:
"""

sql_query(conn, f"""
SELECT 'voc' AS table_name, COUNT(*) AS row_count FROM voc
UNION ALL
SELECT 'sms' AS table_name, COUNT(*) AS row_count FROM sms
UNION ALL
SELECT 'app' AS table_name, COUNT(*) AS row_count FROM app
UNION ALL
SELECT 'user' AS table_name, COUNT(*) AS row_count FROM user;
""")
          
"""
There are about 6000 users and several million SMS messages, voice calls, and app usage records. Let's take a look at the number of unique users in each table:
"""

sql_query(conn, f"""
SELECT 'voc' AS table_name, COUNT(DISTINCT phone_no_m) AS unique_users FROM voc
UNION ALL
SELECT 'sms' AS table_name, COUNT(DISTINCT phone_no_m) AS unique_users FROM sms
UNION ALL
SELECT 'app' AS table_name, COUNT(DISTINCT phone_no_m) AS unique_users FROM app
UNION ALL
SELECT 'user' AS table_name, COUNT(DISTINCT phone_no_m) AS unique_users FROM user;
""")

"""
Since all of these numbers are close to the number of users in the dataset, we can conlude that almost all of the users have SMS records, voice records, and app usage records.
"""

"""
Anamoly detection data are usually highly imbalanced, with the vast majority of training instances being normal. Let's take a look at the number of spammers and non-spammers in the dataset:
"""

sql_query(conn, f"""
SELECT label, COUNT(*) AS row_count FROM user GROUP BY label;
""")

"""
The result of this query tells us that the data are reasonably balanced. About two-thirds of the users are non-spammers and about one-third are spammers.
"""

if st.button("Graph Structure →"):
    switch_page("Graph Structure")