
import streamlit as st

from lib.sql_query import sql_query
from streamlit_extras.switch_page_button import switch_page

conn = st.experimental_connection('snowpark')

print('rendering')

"""
# Feature Engineering

The `user` table, which contains the column indicating whether each user is a frauster or not, has very little information that would likely be useful for detecting fraud:
"""

sql_query(conn, """SELECT * FROM user LIMIT 5;""")


"""
However, we can supplement the existing features by computing aggregate statistics from the other three tables. For example, for each user we can calculate:

- **distinct_outgoing_text_count**: The number of unique phone numbers to which a user has sent text messages.

- **distinct_incoming_call_count**: The number of unique phone numbers from which a user has received voice calls.

- **distinct_outgoing_call_count**: The number of unique phone numbers to which a user has made voice calls.

- **distinct_callbacks**: The number of unique phone numbers that a user has both received a call from and later called back.

- **distinct_incoming_text_count**: The number of unique phone numbers from which a user has received text messages.

- **distinct_textbacks**: The number of unique phone numbers that a user has both received a text message from and later texted back.

We can calculate these quantities using SQL queries. First, we create new tables that represent sender and recipient in different columns:
"""

st.code("""
CREATE TABLE calls AS
    SELECT phone_no_m AS sender, opposite_no_m AS recipient, start_datetime AS timestamp FROM voc WHERE calltype_id = 1
    UNION ALL
    SELECT opposite_no_m AS sender, phone_no_m AS recipient, start_datetime AS timestamp FROM voc WHERE calltype_id = 2;

CREATE TABLE texts AS
    SELECT phone_no_m AS sender, opposite_no_m AS recipient, request_datetime AS timestamp FROM sms WHERE calltype_id = 1
    UNION ALL
    SELECT opposite_no_m AS sender, phone_no_m AS recipient, request_datetime AS timestamp FROM sms WHERE calltype_id = 2;
""", "sql")

"""
Populating these two tables is an important step because otherwise the complexity associated with handling the different `calltype_id` values would otherwise be pushed into the queries below, making them significantly more difficult to read and understand.

Now we can use SQL to calculate the statistics described above:
"""

st.code("""
CREATE OR REPLACE TABLE ml_training_data AS (
    WITH outgoing_texts AS (
        SELECT sender, COUNT(*) AS outgoing_text_count
        FROM texts
        GROUP BY sender
    ),
    distinct_outgoing_texts AS (
        SELECT sender, COUNT(DISTINCT recipient) AS distinct_outgoing_text_count
        FROM texts
        GROUP BY sender
    ),
    incoming_calls AS (
        SELECT recipient, COUNT(*) AS incoming_call_count
        FROM calls
        GROUP BY recipient
    ),
    distinct_incoming_calls AS (
        SELECT recipient, COUNT(DISTINCT sender) AS distinct_incoming_call_count
        FROM calls
        GROUP BY recipient
    ),
    outgoing_calls AS (
        SELECT sender, COUNT(recipient) AS outgoing_call_count
        FROM calls
        GROUP BY sender
    ),
    distinct_outgoing_calls AS (
        SELECT sender, COUNT(DISTINCT recipient) AS distinct_outgoing_call_count
        FROM calls
        GROUP BY sender
    ),
    callbacks AS (
        SELECT c1.sender, COUNT(c1.recipient) AS callbacks
        FROM calls c1
        JOIN calls c2 ON c1.sender = c2.recipient AND c1.recipient = c2.sender
        GROUP BY c1.sender
    ),
    distinct_callbacks AS (
        SELECT c1.sender, COUNT(DISTINCT c1.recipient) AS distinct_callbacks
        FROM calls c1
        JOIN calls c2 ON c1.sender = c2.recipient AND c1.recipient = c2.sender
        GROUP BY c1.sender
    ),
    incoming_texts AS (
        SELECT recipient, COUNT(sender) AS incoming_text_count
        FROM texts
        GROUP BY recipient
    ),
    distinct_incoming_texts AS (
        SELECT recipient, COUNT(DISTINCT sender) AS distinct_incoming_text_count
        FROM texts
        GROUP BY recipient
    ),
    textbacks AS (
        SELECT t1.sender, COUNT(t1.recipient) AS textbacks
        FROM texts t1
        JOIN texts t2 ON t1.sender = t2.recipient AND t1.recipient = t2.sender
        GROUP BY t1.sender
    ),
    distinct_textbacks AS (
        SELECT t1.sender, COUNT(DISTINCT t1.recipient) AS distinct_textbacks
        FROM texts t1
        JOIN texts t2 ON t1.sender = t2.recipient AND t1.recipient = t2.sender
        GROUP BY t1.sender
    )
    SELECT 
        u.phone_no_m,
        COALESCE(u.arpu201908, 0) AS arpu201908,
        COALESCE(u.arpu201909, 0) AS arpu201909,
        COALESCE(u.arpu201910, 0) AS arpu201910,
        COALESCE(u.arpu201911, 0) AS arpu201911,
        COALESCE(u.arpu201912, 0) AS arpu201912,
        COALESCE(u.arpu202001, 0) AS arpu202001,
        COALESCE(u.arpu202002, 0) AS arpu202002,
        COALESCE(u.arpu202003, 0) AS arpu202003,
        COALESCE(ot.outgoing_text_count, 0) AS outgoing_text_count,
        COALESCE(dot.distinct_outgoing_text_count, 0) AS distinct_outgoing_text_count,
        COALESCE(ic.incoming_call_count, 0) AS incoming_call_count,
        COALESCE(dic.distinct_incoming_call_count, 0) AS distinct_incoming_call_count,
        COALESCE(oc.outgoing_call_count, 0) AS outgoing_call_count,
        COALESCE(doc.distinct_outgoing_call_count, 0) AS distinct_outgoing_call_count,
        COALESCE(cb.callbacks, 0) AS callbacks,
        COALESCE(dcb.distinct_callbacks, 0) AS distinct_callbacks,
        COALESCE(it.incoming_text_count, 0) AS incoming_text_count,
        COALESCE(dit.distinct_incoming_text_count, 0) AS distinct_incoming_text_count,
        COALESCE(tb.textbacks, 0) AS textbacks,
        COALESCE(dtb.distinct_textbacks, 0) AS distinct_textbacks
    FROM user u
    LEFT JOIN outgoing_texts ot ON u.phone_no_m = ot.sender
    LEFT JOIN distinct_outgoing_texts dot ON u.phone_no_m = dot.sender
    LEFT JOIN incoming_calls ic ON u.phone_no_m = ic.recipient
    LEFT JOIN distinct_incoming_calls dic ON u.phone_no_m = dic.recipient
    LEFT JOIN outgoing_calls oc ON u.phone_no_m = oc.sender
    LEFT JOIN distinct_outgoing_calls doc ON u.phone_no_m = doc.sender
    LEFT JOIN callbacks cb ON u.phone_no_m = cb.sender
    LEFT JOIN distinct_callbacks dcb ON u.phone_no_m = dcb.sender
    LEFT JOIN incoming_texts it ON u.phone_no_m = it.recipient
    LEFT JOIN distinct_incoming_texts dit ON u.phone_no_m = dit.recipient
    LEFT JOIN textbacks tb ON u.phone_no_m = tb.sender
    LEFT JOIN distinct_textbacks dtb ON u.phone_no_m = dtb.sender
);
""", "sql")

if st.button("Results →"):
    switch_page("Results")