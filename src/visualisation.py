"""Geospatial and metric visualisation utilities."""

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt

_WORLD = None


def _get_world():
    global _WORLD
    if _WORLD is None:
        _WORLD = gpd.read_file(
            "https://naturalearth.s3.amazonaws.com/110m_cultural/"
            "ne_110m_admin_0_countries.zip"
        )
    return _WORLD


def plot_network_map(merged, airports, country_name, ax, show_corrections=True):
    """Plot a country's domestic flight network on a geographic basemap.

    Parameters
    ----------
    merged : DataFrame with Lat_S, Lon_S, Lat_T, Lon_T columns
    airports : full airports DataFrame (used for correction markers)
    country_name : display label
    ax : matplotlib axes
    show_corrections : if True, highlight coordinate-corrected airports
    """
    world = _get_world()
    world.plot(ax=ax, color="#f0f0f0", edgecolor="white")

    ax.plot(
        [merged.Lon_S, merged.Lon_T],
        [merged.Lat_S, merged.Lat_T],
        c="blue",
        alpha=0.15,
        linewidth=0.1,
        zorder=1,
    )

    ax.scatter(merged.Lon_S, merged.Lat_S, c="red", s=5, zorder=2,
               label="Active Airports")

    if show_corrections and "is_corrected" in airports.columns:
        corrected = airports[
            (airports["country"] == country_name) & (airports["is_corrected"])
        ]
        if not corrected.empty:
            ax.scatter(
                corrected.Lon, corrected.Lat,
                c="#00FF00", s=80, edgecolors="black", linewidth=1,
                zorder=3, label="Corrected",
            )

    all_lats = pd.concat([merged.Lat_S, merged.Lat_T])
    all_lons = pd.concat([merged.Lon_S, merged.Lon_T])
    pad = 5
    ax.set_xlim(all_lons.min() - pad, all_lons.max() + pad)
    ax.set_ylim(all_lats.min() - pad, all_lats.max() + pad)

    ax.set_title(f"{country_name}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.legend(loc="lower right", fontsize=8)


def plot_weighted_degree(ranks, sorted_kw, country_name, ax):
    ax.semilogy(ranks, sorted_kw, marker=".", linestyle="-", color="purple",
                alpha=0.6)
    ax.set_title(f"{country_name} (Nodes: {len(ranks)})")
    ax.set_xlabel("Node rank r (descending by k_w)")
    ax.set_ylabel("Weighted degree k_w (log scale)")
    ax.grid(True, which="both", ls="--", alpha=0.3)


def plot_degree_betweenness(x, y, country_name, ax, log=False):
    color = "blue" if log else "purple"
    ax.scatter(x, y, alpha=0.7, s=30, color=color, edgecolors="none")
    ax.set_title(f"{country_name}")
    xlabel = "Node degree k (unweighted)"
    ylabel = "Betweenness centrality C_B"
    if log:
        ax.set_xscale("log")
        ax.set_yscale("log")
        xlabel += " (log)"
        ylabel += " (log)"
        ax.margins(0.4)
        ax.grid(True, which="both", ls="--", alpha=0.3)
    else:
        ax.grid(True, alpha=0.3)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)


def plot_assortativity(k_vals, knn_vals, sorted_k, avg_knn, r_val,
                       country_name, ax):
    ax.scatter(k_vals, knn_vals, alpha=0.7, c="orange", edgecolors="black",
               linewidths=0.3, s=30)
    ax.plot(sorted_k, avg_knn, color="red", linewidth=2, label="Average trend")
    ax.set_title(f"{country_name} | r = {r_val:.3f}")
    ax.set_xlabel("Node degree k (unweighted)")
    ax.set_ylabel("Average neighbour degree k_nn")
    ax.legend()
    ax.grid(True, alpha=0.3)


def plot_kplus_core(ranks, k_plus_curve, peak_rank, peak_val, country_name, ax):
    ax.plot(ranks, k_plus_curve, color="green", linewidth=1.5)
    if peak_rank > 0:
        ax.axvline(x=peak_rank, color="red", linestyle="--",
                   label=f"Core rank r* = {peak_rank}")
        ax.scatter([peak_rank], [peak_val], color="red", s=50, zorder=5)
        ax.annotate(f"max k+ = {peak_val}", xy=(peak_rank, peak_val),
                    xytext=(6, 6), textcoords="offset points")
    ax.set_title(f"{country_name} (Core size ~ {peak_rank})")
    ax.set_xlabel("Node rank r (descending by unweighted degree k)")
    ax.set_ylabel("k+ (links to higher-ranked nodes)")
    ax.legend()
    ax.grid(True, alpha=0.3)
