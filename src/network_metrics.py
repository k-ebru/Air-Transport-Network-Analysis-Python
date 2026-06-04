"""Network metric calculations: weighted degree, betweenness, assortativity
and k+ core and periphery identification."""

import numpy as np
import networkx as nx


def weighted_degree_rank(G):
    """Return arrays of (rank, weighted_degree) sorted in descending order."""
    kw = dict(G.degree(weight="weight"))
    sorted_kw = sorted(kw.values(), reverse=True)
    ranks = np.arange(1, len(sorted_kw) + 1)
    return ranks, np.array(sorted_kw)


def degree_betweenness(G):
    """Return parallel arrays of unweighted degree and normalised betweenness
    centrality for every node."""
    bet = nx.betweenness_centrality(G, weight=None)
    deg = dict(G.degree())
    nodes = list(G.nodes())
    x = np.array([deg[n] for n in nodes], dtype=float)
    y = np.array([bet[n] for n in nodes], dtype=float)
    return x, y


def assortativity(G):
    """Return the degree assortativity coefficient together with per node
    degree and average neighbour degree arrays."""
    r = nx.degree_assortativity_coefficient(G, weight=None)
    knn = nx.average_neighbor_degree(G, weight=None)
    deg = dict(G.degree())

    k_vals = np.array(list(deg.values()))
    knn_vals = np.array([knn[n] for n in deg.keys()])

    # Binned average for the trend line
    k_knn_map = {}
    for k, kn in zip(k_vals, knn_vals):
        k_knn_map.setdefault(int(k), []).append(kn)

    sorted_k = sorted(k_knn_map.keys())
    avg_knn = [np.mean(k_knn_map[k]) for k in sorted_k]

    return r, k_vals, knn_vals, np.array(sorted_k), np.array(avg_knn)


def kplus_core(G):
    """Identify the core boundary using the k+ peak method.

    Nodes are ranked by descending unweighted degree.  For each node at rank r,
    k+(r) is the number of its neighbours with a higher rank (i.e. higher
    degree).  The core boundary r* is the rank at which k+ is maximised; if
    there are ties the last occurrence is chosen.
    """
    deg = dict(G.degree())
    ranked_nodes = sorted(deg.keys(), key=lambda n: deg[n], reverse=True)
    rank_pos = {n: i for i, n in enumerate(ranked_nodes)}

    k_plus_curve = []
    for node in ranked_nodes:
        kp = sum(1 for nb in G.neighbors(node) if rank_pos[nb] < rank_pos[node])
        k_plus_curve.append(kp)

    ranks = np.arange(1, len(ranked_nodes) + 1)

    if not k_plus_curve:
        return ranks, np.array(k_plus_curve), 0, 0

    peak_val = max(k_plus_curve)
    peak_indices = [i for i, x in enumerate(k_plus_curve) if x == peak_val]
    peak_rank = peak_indices[-1] + 1

    return ranks, np.array(k_plus_curve), peak_rank, peak_val
