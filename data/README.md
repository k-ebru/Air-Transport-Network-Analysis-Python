# Data

This project uses one month of flight data and an airport reference dataset.

## Files required

| File | Description |
|------|-------------|
| `Airports.csv` | Airport codes, names, countries and geographic coordinates |
| `Flight Data.xlsx` | Domestic and international flight records with source, target, country and weight columns |

## How to obtain

The datasets are available on [Kaggle](https://www.kaggle.com/) under the search
term "airport flight data". Place the downloaded files in this folder before
running the notebooks.

## Notes

- The airport coordinate errors (positive latitudes for Australian airports,
  incorrect positions for some US airports) are present in the raw data and
  corrected programmatically in `src/data_preprocessing.py`.
- Only domestic flights (source country == target country) are used in the
  analysis.
