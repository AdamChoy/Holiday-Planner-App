-- ================================================================
-- Holiday Planner Database Schema
-- Database: PostgreSQL
-- ================================================================

-- Drop tables if they exist (for clean re-runs)
DROP TABLE IF EXISTS live_data CASCADE;
DROP TABLE IF EXISTS cost_data CASCADE;
DROP TABLE IF EXISTS destinations CASCADE;

-- ================================================================
-- airports
-- UK departure airports for user selection
-- ================================================================
CREATE TABLE airports (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    iata_code   VARCHAR(10)  NOT NULL UNIQUE,
    city        VARCHAR(100) NOT NULL,
    region      VARCHAR(100)
);

-- ================================================================
-- destinations
-- Static destination data — updated manually
-- ================================================================
CREATE TABLE destinations (
    id                  SERIAL PRIMARY KEY,
    name                VARCHAR(100) NOT NULL,
    country             VARCHAR(100) NOT NULL,
    lat                 FLOAT        NOT NULL,
    lon                 FLOAT        NOT NULL,
    iata_code           VARCHAR(10)  NOT NULL,
    currency_code       VARCHAR(10)  NOT NULL,
    language            VARCHAR(100),
    visa_required       BOOLEAN      DEFAULT FALSE,
    best_time_to_visit  VARCHAR(50),
    peak_times          VARCHAR(100),  -- e.g. "July,August"

    -- Vibe scores (1-10)
    beach_score         FLOAT        DEFAULT 5.0,
    nightlife_score     FLOAT        DEFAULT 5.0,
    city_score          FLOAT        DEFAULT 5.0,

    -- LLM generated summary
    description         TEXT,

    created_at          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at          TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
-- cost_data
-- Numbeo scraped data — refreshed weekly
-- ================================================================
CREATE TABLE cost_data (
    id                    SERIAL PRIMARY KEY,
    destination_id        INTEGER REFERENCES destinations(id) ON DELETE CASCADE,
    avg_meal_cost         FLOAT,   -- £ per meal
    cost_of_living_index  FLOAT,   -- Numbeo index
    safety_index          FLOAT,   -- Numbeo safety index (0-100)
    last_updated          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
-- live_data
-- Cached live data — refreshed per user request
-- Prevents hammering APIs on every single request
-- ================================================================
CREATE TABLE live_data (
    id                   SERIAL PRIMARY KEY,
    destination_id       INTEGER REFERENCES destinations(id) ON DELETE CASCADE,

    -- Weather
    avg_temp FLOAT,
    humidity INTEGER,
    cloudiness INTEGER,
    wind_speed FLOAT,
    weather_description  VARCHAR(100),

    -- Flights (cached per origin airport)
    origin_iata VARCHAR(10),
    flight_cost FLOAT,
    flight_duration_hrs  FLOAT,
    stops INTEGER,
    airline VARCHAR(100),

    -- Hotels
    avg_hotel_per_night  FLOAT,
    hotel_name VARCHAR(200),
    hotel_rating FLOAT,

    last_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ================================================================
-- Indexes for faster lookups
-- ================================================================
CREATE TABLE climate_data (
    id SERIAL PRIMARY KEY,
    destination_id INTEGER REFERENCES destinations(id) ON DELETE CASCADE,
    month INTEGER NOT NULL, -- 1-12
    avg_temp FLOAT, -- °C
    avg_humidity INTEGER,  -- %
    avg_rain_days  INTEGER, -- rainy days per month
    description VARCHAR(100),
    CONSTRAINT unique_destination_month UNIQUE (destination_id, month)
);

CREATE INDEX idx_climate_destination ON climate_data(destination_id);
CREATE INDEX idx_destinations_name ON destinations(name);
CREATE INDEX idx_cost_destination ON cost_data(destination_id);
CREATE INDEX idx_live_destination ON live_data(destination_id);
CREATE INDEX idx_live_origin ON live_data(origin_iata);