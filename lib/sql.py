
simple_feature_query = """
CREATE OR REPLACE TABLE simple_features AS (
    WITH outgoing_calls AS (
        SELECT sender, COUNT(*) AS outgoing_call_count, COUNT(DISTINCT recipient) AS distinct_outgoing_call_count
        FROM calls
        GROUP BY sender
    ),
    incoming_calls AS (
        SELECT recipient, COUNT(*) AS incoming_call_count, COUNT(DISTINCT sender) AS distinct_incoming_call_count
        FROM calls
        GROUP BY recipient
    ),
    outgoing_texts AS (
        SELECT sender, COUNT(*) AS outgoing_text_count, COUNT(DISTINCT recipient) AS distinct_outgoing_text_count
        FROM texts
        GROUP BY sender
    ),
    incoming_texts AS (
        SELECT recipient, COUNT(*) AS incoming_text_count, COUNT(DISTINCT sender) AS distinct_incoming_text_count
        FROM texts
        GROUP BY recipient
    ),
    callbacks AS (
        SELECT c1.sender, COUNT(c1.recipient) AS callbacks, COUNT(DISTINCT c1.recipient) AS distinct_callbacks
        FROM calls c1
        JOIN calls c2 ON c1.sender = c2.recipient AND c1.recipient = c2.sender
        GROUP BY c1.sender
    ),
    textbacks AS (
        SELECT t1.sender, COUNT(t1.recipient) AS textbacks, COUNT(DISTINCT t1.recipient) AS distinct_textbacks
        FROM texts t1
        JOIN texts t2 ON t1.sender = t2.recipient AND t1.recipient = t2.sender
        GROUP BY t1.sender
    )
    SELECT 
        u.phone_no_m,
        COALESCE(oc.outgoing_call_count, 0) AS outgoing_call_count,
        COALESCE(oc.distinct_outgoing_call_count, 0) AS distinct_outgoing_call_count,
        COALESCE(ic.incoming_call_count, 0) AS incoming_call_count,
        COALESCE(ic.distinct_incoming_call_count, 0) AS distinct_incoming_call_count,
        COALESCE(ot.outgoing_text_count, 0) AS outgoing_text_count,
        COALESCE(ot.distinct_outgoing_text_count, 0) AS distinct_outgoing_text_count,
        COALESCE(it.incoming_text_count, 0) AS incoming_text_count,
        COALESCE(it.distinct_incoming_text_count, 0) AS distinct_incoming_text_count,
        COALESCE(cb.callbacks, 0) AS callbacks,
        COALESCE(cb.distinct_callbacks, 0) AS distinct_callbacks,
        COALESCE(tb.textbacks, 0) AS textbacks,
        COALESCE(tb.distinct_textbacks, 0) AS distinct_textbacks,
        CASE WHEN COALESCE(ic.incoming_call_count, 0) > 0 THEN COALESCE(oc.outgoing_call_count, 0) / COALESCE(ic.incoming_call_count, 0) ELSE 0 END AS call_in_out_ratio,
        CASE WHEN COALESCE(oc.outgoing_call_count, 0) > 0 THEN COALESCE(cb.callbacks, 0) / COALESCE(oc.outgoing_call_count, 0) ELSE 0 END AS call_out_callback_ratio,
        CASE WHEN COALESCE(ic.distinct_incoming_call_count, 0) > 0 THEN COALESCE(oc.distinct_outgoing_call_count, 0) / COALESCE(ic.distinct_incoming_call_count, 0) ELSE 0 END AS distinct_call_in_out_ratio,
        CASE WHEN COALESCE(it.incoming_text_count, 0) > 0 THEN COALESCE(ot.outgoing_text_count, 0) / COALESCE(it.incoming_text_count, 0) ELSE 0 END AS text_in_out_ratio,
        CASE WHEN COALESCE(ot.outgoing_text_count, 0) > 0 THEN COALESCE(tb.textbacks, 0) / COALESCE(ot.outgoing_text_count, 0) ELSE 0 END AS text_out_textback_ratio,
        CASE WHEN COALESCE(ot.outgoing_text_count, 0) + COALESCE(it.incoming_text_count, 0) > 0 THEN COALESCE(ot.outgoing_text_count, 0) / (COALESCE(ot.outgoing_text_count, 0) + COALESCE(it.incoming_text_count, 0)) ELSE 0 END AS text_out_total_ratio
    FROM user u
    LEFT JOIN outgoing_calls oc ON u.phone_no_m = oc.sender
    LEFT JOIN incoming_calls ic ON u.phone_no_m = ic.recipient
    LEFT JOIN outgoing_texts ot ON u.phone_no_m = ot.sender
    LEFT JOIN incoming_texts it ON u.phone_no_m = it.recipient
    LEFT JOIN callbacks cb ON u.phone_no_m = cb.sender
    LEFT JOIN textbacks tb ON u.phone_no_m = tb.sender
);
"""