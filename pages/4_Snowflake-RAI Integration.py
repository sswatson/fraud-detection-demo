
import streamlit as st

from lib.util import set_page_config
set_page_config()

"""
# Snowflake-RAI Integration

In this section, we'll look at how to integrate RelationalAI with Snowflake and use it to calculate graph quantities of interest.

## Setup

Snowflake account admins can create and inspect a RelationalAI integration using the following commands from a Snowflake SQL worksheet:

```sql
CREATE SERVICE rai;
SHOW SERVICES;
DESC SERVICE rai;
```

*Note: this does not exist yet. This is part of what we're announcing, not launching.*

## Data Streams

To perform graph computations on a table, first create a data stream from the table:

```sql
call create_data_stream(
    'snowflake_table_name',
    'your_rai_database',
    'rai_table_name',
);
```

## Graph Analysis

To calcluate PageRank, for example: 

```sql
select *
FROM Table(
    relgraphlib(
        'your-rel-engine',
        'your-rel-db',
        'rel-table-name',
        'first-column-name',
        'second-column-name',
        'pagerank'
    )
);
```

"""
