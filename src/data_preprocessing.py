"""Data loading, cleaning and airport coordinate correction."""

import pandas as pd


def load_data(airports_path, flights_path):
    """Load airports and flights datasets with standardised column names."""
    airports = pd.read_csv(airports_path, encoding="latin1")
    flights = pd.read_excel(flights_path)

    airports.columns = airports.columns.str.strip()
    flights.columns = flights.columns.str.strip()

    airports["id"] = airports["id"].astype(str).str.strip().str.upper()
    flights["Source"] = flights["Source"].astype(str).str.strip().str.upper()
    flights["Target"] = flights["Target"].astype(str).str.strip().str.upper()

    airports["Lat"] = pd.to_numeric(airports["Lat"], errors="coerce")
    airports["Lon"] = pd.to_numeric(airports["Lon"], errors="coerce")

    airports["country"] = airports["country"].replace({"United States": "USA"})

    return airports, flights


def check_missing_codes(airports, flights):
    """Identify flight records that reference airport codes absent from the
    airports table."""
    airport_codes = set(airports["id"])
    source_codes = set(flights["Source"])
    target_codes = set(flights["Target"])

    missing_source = source_codes - airport_codes
    missing_target = target_codes - airport_codes
    all_missing = missing_source | missing_target

    return {
        "missing_source": missing_source,
        "missing_target": missing_target,
        "total_missing": len(all_missing),
    }


def correct_coordinates(airports):
    """Fix known coordinate errors for Australia and the USA.

    Australia: airports recorded with positive latitude are mirrored to the
    southern hemisphere.  USA: eight airports with incorrect positions are
    corrected using publicly available location data.

    Only coordinates are changed — all network connections are preserved.
    """
    airports = airports.copy()
    airports["is_corrected"] = False

    # Australia — positive latitudes should be negative
    aus_mask = (airports["country"] == "Australia") & (airports["Lat"] > 0)
    airports.loc[aus_mask, "is_corrected"] = True
    airports.loc[aus_mask, "Lat"] = airports.loc[aus_mask, "Lat"] * -1

    # USA — manually corrected airports
    usa_corrections = {
        "SYL": {"Lat": 35.7197, "Lon": -120.7633},
        "ARA": {"Lat": 30.0378, "Lon": -91.8839},
        "DGN": {"Lat": 38.3275, "Lon": -77.1033},
        "CWO": {"Lat": 32.8116, "Lon": -98.0624},
        "BSF": {"Lat": 19.7600, "Lon": -155.5539},
        "AHC": {"Lat": 40.2659, "Lon": -120.1506},
        "TCT": {"Lat": 62.9932, "Lon": -156.0290},
        "WSD": {"Lat": 32.3410, "Lon": -106.4030},
    }

    for code, coords in usa_corrections.items():
        mask = airports["id"] == code
        if mask.any():
            airports.loc[mask, ["Lat", "Lon"]] = [coords["Lat"], coords["Lon"]]
            airports.loc[mask, "is_corrected"] = True

    return airports


def get_domestic_flights(flights, country):
    """Filter flights where both source and target belong to the same
    country."""
    return flights[
        (flights["Source Country"] == country)
        & (flights["Target Country"] == country)
    ].copy()


def merge_coordinates(domestic_flights, airports):
    """Attach source and target airport coordinates to each flight record."""
    cols = ["id", "Lat", "Lon"]
    merged = domestic_flights.merge(
        airports[cols], left_on="Source", right_on="id"
    ).rename(columns={"Lat": "Lat_S", "Lon": "Lon_S"})
    merged = merged.merge(
        airports[cols], left_on="Target", right_on="id"
    ).rename(columns={"Lat": "Lat_T", "Lon": "Lon_T"})
    return merged
