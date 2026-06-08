# Air Transport Network Analysis with Python

This project studies domestic air transport networks in the United States,
China, the United Kingdom and Australia using one month of flight data.

I built it to look beyond the obvious question of which airports are busiest.
The analysis compares traffic concentration, bridge airports, hub dependence and
the size of each country's network core.

![Cleaned domestic air transport networks](figures/cleaned_network_maps.png)

## Problem Statement

In an air network, airport importance is not only about flight volume. An
airport can also matter because it connects distant regions or sits between
parts of the network that would otherwise be weakly connected.

This project asks:

1. Which airports and routes carry the most domestic traffic?
2. Which airports act as bridges?
3. Which countries are more dependent on a small number of hubs?
4. What does the network structure suggest about resilience?

## Dataset

The project uses two files in the `data/` folder.

| File | What it contains |
| --- | --- |
| `data/Airports.csv` | Airport code, airport name, country and coordinates |
| `data/Flight Data.xlsx` | Source airport, target airport, countries and route weight |

Only domestic flights are used, so the source country and target country must
match. I also corrected visible coordinate errors in the airport table before
creating the maps.

## Methods

I built an undirected weighted graph for each country. Airports are nodes, and
domestic routes are weighted edges. If the same route appears more than once,
the route weights are summed.

The main metrics are:

1. Weighted degree, to rank airports by traffic volume.
2. Betweenness centrality, to find bridge airports.
3. Degree assortativity, to measure how strongly hubs connect to smaller
   airports.
4. k+ core size, to estimate the central group of airports in the network.

I also added SQL queries for the same type of checks in a relational format:
country summaries, top hubs and busiest route pairs.

## Results

| Country | GDP rank used as context | Assortativity | Core size | Main reading |
| --- | ---: | ---: | ---: | --- |
| United States | 1 | -0.198 | 41 | Large core, strong hub and spoke behaviour, and several bridge airports |
| China | 2 | -0.397 | 23 | The most hub focused network in this comparison |
| United Kingdom | 6 | -0.119 | 16 | Compact network with less extreme hub dependence |
| Australia | 15 | -0.230 | 9 | Small core shaped by long distances and remote area connectivity |

The clearest pattern is that volume and structural importance are not the same.
Some airports are important because they handle a lot of traffic. Others are
important because they connect regions that would otherwise be harder to reach.

China has the strongest negative assortativity, which points to a more
hub dependent structure. The United States has the largest core, meaning that
important network functions are spread across more airports. Australia has a
smaller core, but distance makes several airports strategically important.

## Country Notes

**United States.** The network is large and geographically spread out. It has a
clear hub and spoke pattern, but some airports with moderate degree still have
high betweenness because they connect isolated regions.

**China.** The network is dense in the east and sparser in the west. Its strong
negative assortativity suggests that major hubs carry a lot of the network
structure.

**United Kingdom.** The network is compact, with shorter domestic distances and
a weaker link between degree and betweenness. That points to a more distributed
domestic structure.

**Australia.** Long distance links matter more here. Several airports have value
because they connect remote areas, even when they are not the largest by direct
traffic volume.

## Figures

| Cleaned spatial networks | Weighted degree ranking |
| --- | --- |
| ![Cleaned domestic networks](figures/cleaned_network_maps.png) | ![Weighted degree ranking](figures/weighted_degree_rank.png) |

| Assortativity | Core and periphery |
| --- | --- |
| ![Assortativity](figures/assortativity.png) | ![Core and periphery](figures/core_periphery.png) |

## How to Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Open the notebooks in this order:

1. `notebooks/01_data_cleaning_and_network_construction.ipynb`
2. `notebooks/02_network_metrics_analysis.ipynb`
3. `notebooks/03_operational_interpretation.ipynb`

The map function uses a Natural Earth basemap when internet access is available.
If the basemap cannot be downloaded, the notebooks still run and plot the routes
and airport points without the background map.

## SQL

The `sql/` folder shows how I would reproduce the main checks if the data were
loaded into PostgreSQL style tables.

| File | Purpose |
| --- | --- |
| `01_create_tables.sql` | Table structure and indexes |
| `02_domestic_flight_summary.sql` | Domestic flight summaries by country |
| `03_top_airport_hubs.sql` | Top airport hubs using weighted degree logic |
| `04_route_volume_analysis.sql` | Busiest domestic route pairs |

The Python notebooks remain the main analysis because the network metrics need
NetworkX.

## Dependencies

Python, pandas, NumPy, NetworkX, GeoPandas, Matplotlib, openpyxl and SQL.
Install the package ranges with:

```bash
pip install -r requirements.txt
```

## My Contribution

I did the full workflow: data cleaning, coordinate correction, graph building,
metric calculation, SQL checks, figures and interpretation.

The part I focused on most was interpretation. I wanted the project to say more
than "these are the biggest airports". The final analysis connects the metrics
to hub dependence, bridge airports, route concentration and network resilience.

## Repository Structure

```text
air-transport-network-analysis-python/
  data/
  figures/
  notebooks/
  sql/
  src/
  README.md
  requirements.txt
```

## References

1. Guo et al. (2019), *Global air transport complex network: multi scale analysis*
2. Ersoz and Aldemir (2024), complex network analysis of European air transport
3. Nominal GDP country ranking used as context in the original analysis
