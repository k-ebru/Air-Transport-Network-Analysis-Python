-- Identify the top 20 domestic airport hubs by total connection volume.
-- Hub importance is measured by weighted degree (sum of flight volumes).

SELECT
    f.source              AS airport_code,
    a.airport_name,
    f.source_country      AS country,
    COUNT(DISTINCT f.target) AS unique_destinations,
    SUM(f.weight)         AS total_flight_volume
FROM flights f
JOIN airports a ON f.source = a.airport_id
WHERE f.source_country = f.target_country
GROUP BY f.source, a.airport_name, f.source_country
ORDER BY total_flight_volume DESC
LIMIT 20;
