/*
Aggregate domestic flight statistics for the four countries analysed in the
Python notebooks.
*/

SELECT
    source_country                  AS country,
    COUNT(*)                        AS domestic_records,
    COUNT(DISTINCT source)          AS unique_source_airports,
    COUNT(DISTINCT target)          AS unique_target_airports,
    SUM(weight)                     AS total_flight_volume
FROM flights
WHERE source_country = target_country
  AND source_country IN ('USA', 'China', 'United Kingdom', 'Australia')
GROUP BY source_country
ORDER BY total_flight_volume DESC;
