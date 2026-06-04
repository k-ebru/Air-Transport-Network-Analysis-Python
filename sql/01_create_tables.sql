-- Schema definition for the air transport network analysis.
-- Designed for PostgreSQL-style relational analysis.
--
-- The airport reference file can contain the same airport code in more than
-- one country, so airport_code is indexed but not used as the primary key.
-- Expected airport column mapping from the CSV:
-- id -> airport_code, label -> airport_name, Lat -> latitude, Lon -> longitude.

CREATE TABLE IF NOT EXISTS airports (
    airport_key  BIGSERIAL PRIMARY KEY,
    airport_code VARCHAR(10) NOT NULL,
    airport_name VARCHAR(200),
    city         VARCHAR(100),
    country      VARCHAR(100),
    latitude     DECIMAL(9, 6),
    longitude    DECIMAL(9, 6)
);

CREATE TABLE IF NOT EXISTS flights (
    flight_id      BIGSERIAL PRIMARY KEY,
    source         VARCHAR(10) NOT NULL,
    target         VARCHAR(10) NOT NULL,
    source_country VARCHAR(100),
    target_country VARCHAR(100),
    weight         INTEGER DEFAULT 1
);

CREATE INDEX idx_airports_code_country ON airports(airport_code, country);
CREATE INDEX idx_flights_source_country ON flights(source_country);
CREATE INDEX idx_flights_target_country ON flights(target_country);
CREATE INDEX idx_flights_source ON flights(source);
CREATE INDEX idx_flights_target ON flights(target);
