# Air Transport Network Analysis with Python

This project studies domestic air transport networks in the **United States,
China, the United Kingdom and Australia** using one month of flight data.

I built it to understand more than just "which airports are busy". The analysis
looks at how traffic is concentrated, which airports act as transfer points, how
robust each domestic network is, and how geography and economic scale help
explain the differences between countries.

## What I Analysed

- cleaned airport coordinates and corrected visible geospatial errors
- built domestic flight networks with airports as nodes and flights as weighted edges
- compared weighted degree, betweenness centrality, assortativity and core size
- interpreted the results by country, not only as charts
- used GDP ranking as external context for the core-periphery comparison
- added SQL queries that mirror the same airport and route checks in a relational format

## Main Findings

| Country | GDP rank used as context | Assortativity | Core size | Main interpretation |
|---|---:|---:|---:|---|
| United States | 1 | -0.198 | 41 | Large network core with strong hub-spoke behaviour and some critical bridge airports |
| China | 2 | -0.397 | 23 | Most hub-focused network, with traffic strongly concentrated around major eastern hubs |
| United Kingdom | 6 | -0.119 | 16 | More compact and distributed network, with less extreme hub dependence |
| Australia | 15 | -0.230 | 9 | Coastal hub-spoke network shaped by long distances and a small number of key hubs |

The core-periphery result was one of the most interesting parts of the project.
The larger economies in the comparison have larger network cores. This suggests
that more airports share the important network functions, which can improve
robustness, even if it is not always the most economically efficient structure.

## Country Notes

**United States:** the network is large and geographically spread out. It has a
clear hub-spoke pattern, but one moderate-degree airport has very high
betweenness. I interpreted this as a bridge role for more isolated regions such
as Alaska or Hawaii.

**China:** the network is dense in the east and much sparser in the west. It has
the strongest negative assortativity, meaning large hubs mainly connect to
smaller airports. This is efficient, but it also creates dependence on a few
major hubs.

**United Kingdom:** the network is compact, with shorter domestic distances and
a weaker link between degree and betweenness. This points to a more distributed
multi-hub structure.

**Australia:** airports are mostly coastal and long-distance links are important.
Several airports have strategic value because they connect remote areas, even
when they are not the largest by direct flight volume.

## Fuel Price Interpretation

I also used the Random Geometric Graph idea from the literature to think about
future network changes. In this framework, the probability of a connection
depends on distance and a distance-penalty parameter. I treated that parameter
as a proxy for fuel price and operating cost.

When fuel prices are high, long-distance routes become less attractive. Large
countries such as the USA and Australia would be more affected, and smaller or
medium-sized aircraft may become more suitable on some routes. When fuel prices
are low, long-distance hub-spoke links become easier to maintain, so large hubs
and high-capacity aircraft become more important again.

## Selected Figures

| Cleaned spatial networks | Weighted degree rank |
|---|---|
| ![Cleaned domestic networks](figures/cleaned_network_maps.png) | ![Weighted degree rank](figures/weighted_degree_rank.png) |

| Assortativity | Core-periphery |
|---|---|
| ![Assortativity](figures/assortativity.png) | ![Core-periphery](figures/core_periphery.png) |

## Repository Structure

```text
air-transport-network-analysis-python/
├── data/          # input airport and flight datasets
├── figures/       # saved outputs used in this README
├── notebooks/     # analysis workflow in three notebooks
├── sql/           # relational versions of the main checks
├── src/           # reusable Python functions
├── README.md
└── requirements.txt
```

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Then open the notebooks in order:

1. `notebooks/01_data_cleaning_and_network_construction.ipynb`
2. `notebooks/02_network_metrics_analysis.ipynb`
3. `notebooks/03_operational_interpretation.ipynb`

The map function uses a Natural Earth basemap when internet access is available.
If the basemap cannot be downloaded, the analysis still runs and plots the routes
and airport points without the background map.

## SQL Folder

The SQL files show how I would reproduce the main checks if the flight data were
loaded into a PostgreSQL-style relational database. They cover:

- table structure for airport and flight records
- domestic flight summaries for the four analysed countries
- airport hub ranking using source and target traffic volume
- busiest domestic route pairs

The Python notebooks remain the main analysis because the network metrics
require graph operations from NetworkX.

## References Used in the Analysis

- Guo et al. (2019), *Global air transport complex network: multi-scale analysis*
- Ersoz and Aldemir (2024), complex network analysis of European air transport
- GDP ranking context from the nominal GDP country ranking used in the original analysis

## Tech Stack

Python, pandas, NumPy, NetworkX, GeoPandas, Matplotlib, SQL
