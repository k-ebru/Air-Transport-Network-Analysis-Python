-- Schema definition for the air transport network analysis.
-- Designed for PostgreSQL but compatible with most SQL dialects.

CREATE TABLE IF NOT EXISTS airports (
    airport_id   VARCHAR(10) PRIMARY KEY,
    airport_name VARCHAR(200),
    city         VARCHAR(100),
    country      VARCHAR(100),
    latitude     DECIMAL(9, 6),
    longitude    DECIMAL(9, 6)
);

CREATE TABLE IF NOT EXISTS flights (
    flight_id      SERIAL PRIMARY KEY,
    source         VARCHAR(10) NOT NULL REFERENCES airports(airport_id),
    target         VARCHAR(10) NOT NULL REFERENCES airports(airport_id),
    source_country VARCHAR(100),
    target_country VARCHAR(100),
    weight         INTEGER DEFAULT 1
);

CREATE INDEX idx_flights_source_country ON flights(source_country);
CREATE INDEX idx_flights_target_country ON flights(target_country);
CREATE INDEX idx_flights_source ON flights(source);
CREATE INDEX idx_flights_target ON flights(target);
