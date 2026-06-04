/*
Identify the top domestic airport hubs by weighted degree.

The Python graph is undirected, so this query counts both outgoing and incoming
domestic traffic for each airport before ranking hubs.
*/

WITH domestic_links AS (
    SELECT
        source_country AS country,
        source         AS airport_code,
        target         AS connected_airport,
        weight
    FROM flights
    WHERE source_country = target_country
      AND source_country IN ('USA', 'China', 'United Kingdom', 'Australia')

    UNION ALL

    SELECT
        target_country AS country,
        target         AS airport_code,
        source         AS connected_airport,
        weight
    FROM flights
    WHERE source_country = target_country
      AND target_country IN ('USA', 'China', 'United Kingdom', 'Australia')
),
airport_lookup AS (
    SELECT
        airport_code,
        airport_name,
        CASE
            WHEN country = 'United States' THEN 'USA'
            ELSE country
        END AS country
    FROM airports
)

SELECT
    d.country,
    d.airport_code,
    MAX(a.airport_name)              AS airport_name,
    COUNT(DISTINCT d.connected_airport) AS unique_connections,
    SUM(d.weight)                    AS weighted_degree
FROM domestic_links d
LEFT JOIN airport_lookup a
    ON d.airport_code = a.airport_code
   AND d.country = a.country
GROUP BY d.country, d.airport_code
ORDER BY weighted_degree DESC
LIMIT 20;
