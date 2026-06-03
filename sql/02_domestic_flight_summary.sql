-- Aggregate domestic flight statistics per country.
-- Filters for flights where both endpoints are in the same country.

SELECT
    source_country                  AS country,
    COUNT(*)                        AS domestic_flight_count,
    COUNT(DISTINCT source)          AS unique_source_airports,
    COUNT(DISTINCT target)          AS unique_target_airports,
    SUM(weight)                     AS total_flight_volume
FROM flights
WHERE source_country = target_country
GROUP BY source_country
ORDER BY domestic_flight_count DESC;
