# Data

This project uses one month of flight data and an airport reference dataset.
Both files are included in this folder so the notebooks can be rerun.

## Files

| File | Description |
|------|-------------|
| `Airports.csv` | Airport codes, names, countries and geographic coordinates |
| `Flight Data.xlsx` | Domestic and international flight records with source, target, country and weight columns |

## Notes

- The airport coordinate errors (positive latitudes for Australian airports,
  incorrect positions for some US airports) are present in the raw data and
  corrected programmatically in `src/data_preprocessing.py`.
- Only domestic flights (source country == target country) are used in the
  analysis.
- The airport reference file contains one duplicated airport code (`HRZ`) for
  different countries. The Python analysis uses the country-filtered flight
  records, and the SQL schema avoids treating airport code alone as a unique
  primary key.
