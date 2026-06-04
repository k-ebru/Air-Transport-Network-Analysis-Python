/*
Analyse the busiest domestic route pairs in the four selected countries.
Source and target records are combined into the same route.
*/

WITH ranked_routes AS (
    SELECT
        LEAST(source, target)       AS airport_a,
        GREATEST(source, target)    AS airport_b,
        source_country              AS country,
        SUM(weight)                 AS route_volume,
        ROW_NUMBER() OVER (
            PARTITION BY source_country
            ORDER BY SUM(weight) DESC
        ) AS route_rank
    FROM flights
    WHERE source_country = target_country
      AND source_country IN ('USA', 'China', 'United Kingdom', 'Australia')
    GROUP BY LEAST(source, target), GREATEST(source, target), source_country
)
SELECT
    country,
    airport_a,
    airport_b,
    route_volume,
    route_rank
FROM ranked_routes
WHERE route_rank <= 10
ORDER BY country, route_rank;
