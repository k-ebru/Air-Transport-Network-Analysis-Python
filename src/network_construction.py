"""Build undirected weighted graphs from domestic flight records."""

import numpy as np
import networkx as nx


def build_graph(flights, country):
    """Construct an undirected weighted graph for a country's domestic
    flights.

    Self-loops are removed.  Parallel flights between the same pair of
    airports are aggregated by summing their weights.
    """
    df = flights[
        (flights["Source Country"] == country)
        & (flights["Target Country"] == country)
    ].copy()
    df = df[df["Source"] != df["Target"]]

    # Canonical edge ordering so (A, B) and (B, A) collapse to one edge
    src_tgt = np.sort(df[["Source", "Target"]].values, axis=1)
    df["u"] = src_tgt[:, 0]
    df["v"] = src_tgt[:, 1]
    edge_weights = df.groupby(["u", "v"])["Weight"].sum().reset_index()

    G = nx.Graph()
    for _, row in edge_weights.iterrows():
        G.add_edge(row["u"], row["v"], weight=row["Weight"])
    return G
