
import streamlit as st

from lib.util import page_setup, next_page

page_setup()

"""
# Snowflake-RAI Integration

The simple features in the previous section are *local* graph quantities. For example, a user's callback count can be computed from information about the user's calls with their neighors in the graph. These computations can be handled in plain SQL.

However, often in fraud detection the key information that you want to make available to the machine learning model pertains to non-local structure. Examples of non-local graph structure include:

- The size of a node's connected component. This is the number of nodes that are reachable from the node by following edges.
- Each node's *PageRank* score. This is the probability that a long-running random walk on the graph will end up at the node.
- The *Eigenvector Centrality* of each node. This is a measure of how well-connected a node is to other well-connected nodes.

Because of the complex algorithms required to compute these quantities, computing them in plain SQL is very difficult. Therefore, developers usually use an external graph library for this purpose. While there are several graph analytics technologies, RelationalAI offers some unique benefits:

1. Seamless integration with Snowflake. You can use the same SQL query to compute graph features as you would use to compute simple features.
2. Cloud-native architecture. This means that you can use RelationalAI on datasets that are too large to fit on a single node.

In this section, we'll talk about how to use RelationalAI to compute graph features. In the next section, we'll look at how the model's performance improves when we have these quantities available.

## Setup

*Note: This section will have to be revisited once the API has stabilized, and/or we decide what we want to show here instead. For now I'm using what's in the Getting Started doc as a placeholder.*

*Note: This is the part where we want to transition to showing steps in a Snowflake worksheet. This is difficult to record currently because the steps don't work yet. Also, there are some arguments in the example calls that don't really make sense to require users to think about, and they will probably be dropped before the final version*.

Snowflake account admins can create and inspect a RelationalAI integration using instructions provided by RelationalAI. We'll assume that the integration is set up and show how to use it.

## Data Streams

To perform graph computations on a table, first create a *data stream* from the table:

```sql
call create_data_stream(
    'snowflake_table_name',
    'your_rai_database',
    'rai_table_name',
);
```

Once the data stream is set up, it will update the RelationalAI relation automatically as the Snowflake table changes.

## Graph Analysis

You can run graph algorithms on the data stream using the `relgraphlib` function. Here's an example showing how to calculate PageRank:

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

next_page("Graph Analysis")