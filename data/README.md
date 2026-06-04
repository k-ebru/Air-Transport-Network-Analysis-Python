# Data

This project uses one month of flight data and an airport reference dataset.
Both files are included in this folder so the notebooks can be rerun.

## Files

<table>
  <tr>
    <th>File</th>
    <th>Description</th>
  </tr>
  <tr>
    <td><code>Airports.csv</code></td>
    <td>Airport codes, names, countries and geographic coordinates</td>
  </tr>
  <tr>
    <td><code>Flight Data.xlsx</code></td>
    <td>Domestic and international flight records with source, target, country and weight columns</td>
  </tr>
</table>

## Notes

The airport coordinate errors are present in the raw data and corrected
programmatically in `src/data_preprocessing.py`. These include positive latitude
values for some Australian airports and incorrect positions for some US
airports.

Only domestic flights are used in the analysis, where source country equals
target country.

The airport reference file contains one duplicated airport code, `HRZ`, for
different countries. The Python analysis uses country filtered flight records,
and the SQL schema avoids treating airport code alone as a unique primary key.
