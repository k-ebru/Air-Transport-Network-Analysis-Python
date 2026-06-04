# Air Transport Network Analysis with Python

This project studies domestic air transport networks in the **United States,
China, the United Kingdom and Australia** using one month of flight data.

I built it to understand more than just "which airports are busy". The analysis
looks at how traffic is concentrated, which airports act as transfer points, how
robust each domestic network is, and how geography and economic scale help
explain the differences between countries.

## What I Analysed

I cleaned visible coordinate errors in the airport data, built domestic flight
networks with airports as nodes and flights as weighted edges, and compared the
countries using weighted degree, betweenness centrality, assortativity and core
size. I also used GDP ranking as economic context for the core and periphery
comparison, then added SQL queries for the same airport and route checks in a
relational format.

## Main Findings

<table>
  <tr>
    <th>Country</th>
    <th>GDP rank used as context</th>
    <th>Assortativity</th>
    <th>Core size</th>
    <th>Main interpretation</th>
  </tr>
  <tr>
    <td>United States</td>
    <td>1</td>
    <td>&minus;0.198</td>
    <td>41</td>
    <td>Large network core with strong hub and spoke behaviour and some critical bridge airports</td>
  </tr>
  <tr>
    <td>China</td>
    <td>2</td>
    <td>&minus;0.397</td>
    <td>23</td>
    <td>Most hub focused network, with traffic strongly concentrated around major eastern hubs</td>
  </tr>
  <tr>
    <td>United Kingdom</td>
    <td>6</td>
    <td>&minus;0.119</td>
    <td>16</td>
    <td>More compact and distributed network, with less extreme hub dependence</td>
  </tr>
  <tr>
    <td>Australia</td>
    <td>15</td>
    <td>&minus;0.230</td>
    <td>9</td>
    <td>Coastal hub and spoke network shaped by long distances and a small number of key hubs</td>
  </tr>
</table>

The core and periphery result was one of the most interesting parts of the project.
The larger economies in the comparison have larger network cores. This suggests
that more airports share the important network functions, which can improve
robustness, even if it is not always the most economically efficient structure.

## Country Notes

**United States:** the network is large and geographically spread out. It has a
clear hub and spoke pattern, but one airport with moderate degree has very high
betweenness. I interpreted this as a bridge role for more isolated regions such
as Alaska or Hawaii.

**China:** the network is dense in the east and much sparser in the west. It has
the strongest negative assortativity, meaning large hubs mainly connect to
smaller airports. This is efficient, but it also creates dependence on a few
major hubs.

**United Kingdom:** the network is compact, with shorter domestic distances and
a weaker link between degree and betweenness. This points to a more distributed
network with several important hubs.

**Australia:** airports are mostly coastal and long distance links are important.
Several airports have strategic value because they connect remote areas, even
when they are not the largest by direct flight volume.

## Fuel Price Interpretation

I also used the Random Geometric Graph idea from the literature to think about
future network changes. In this framework, the probability of a connection
depends on distance and a distance penalty parameter. I treated that parameter
as a proxy for fuel price and operating cost.

When fuel prices are high, long distance routes become less attractive. Large
countries such as the USA and Australia would be more affected, and smaller or
medium sized aircraft may become more suitable on some routes. When fuel prices
are low, long distance hub links become easier to maintain, so large hubs and
high capacity aircraft become more important again.

## Selected Figures

<table>
  <tr>
    <th>Cleaned spatial networks</th>
    <th>Weighted degree rank</th>
  </tr>
  <tr>
    <td><img src="figures/cleaned_network_maps.png" alt="Cleaned domestic networks"></td>
    <td><img src="figures/weighted_degree_rank.png" alt="Weighted degree rank"></td>
  </tr>
  <tr>
    <th>Assortativity</th>
    <th>Core and periphery</th>
  </tr>
  <tr>
    <td><img src="figures/assortativity.png" alt="Assortativity"></td>
    <td><img src="figures/core_periphery.png" alt="Core and periphery"></td>
  </tr>
</table>

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
loaded into a PostgreSQL style relational database.

The queries cover the table structure, domestic flight summaries for the four
countries, airport hub ranking using source and target traffic volume, and the
busiest domestic route pairs.

The Python notebooks remain the main analysis because the network metrics
require graph operations from NetworkX.

## References Used in the Analysis

1. Guo et al. (2019), *Global air transport complex network: multi scale analysis*
2. Ersoz and Aldemir (2024), complex network analysis of European air transport
3. GDP ranking context from the nominal GDP country ranking used in the original analysis

## Tech Stack

Python, pandas, NumPy, NetworkX, GeoPandas, Matplotlib, SQL
