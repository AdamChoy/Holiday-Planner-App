"""
db.py
-----
PostgreSQL database connection and query functions.
Uses psycopg2 for direct SQL queries.

Usage:
    from backend.database.db import get_all_destinations, get_cost_data
"""

import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    """
    Creates and returns a PostgreSQL database connection.

    Returns:
        psycopg2 connection object
    """
    return psycopg2.connect(
        host=os.getenv("DB_HOST",     "localhost"),
        port=os.getenv("DB_PORT",     5432),
        dbname=os.getenv("DB_NAME",   "holiday_planner"),
        user=os.getenv("DB_USER",     "postgres"),
        password=os.getenv("DB_PASSWORD")
    )


def get_all_destinations() -> list[dict]:
    """
    Returns all destinations joined with their cost data.

    Returns:
        List of destination dicts with cost data included
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    d.id,
                    d.name,
                    d.country,
                    d.lat,
                    d.lon,
                    d.iata_code,
                    d.currency_code,
                    d.language,
                    d.visa_required,
                    d.best_time_to_visit,
                    d.peak_times,
                    d.beach_score,
                    d.nightlife_score,
                    d.city_score,
                    d.description,
                    c.avg_meal_cost,
                    c.cost_of_living_index,
                    c.safety_index
                FROM destinations d
                LEFT JOIN cost_data c ON c.destination_id = d.id
                ORDER BY d.name ASC
            """)
            return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()


def get_destination_by_name(name: str) -> dict:
    """
    Returns a single destination by name.

    Args:
        name: Destination name e.g. "Barcelona"

    Returns:
        Destination dict or None if not found
    """
    conn = get_connection()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("""
                SELECT
                    d.*,
                    c.avg_meal_cost,
                    c.cost_of_living_index,
                    c.safety_index
                FROM destinations d
                LEFT JOIN cost_data c ON c.destination_id = d.id
                WHERE LOWER(d.name) = LOWER(%s)
            """, (name,))
            row = cur.fetchone()
            return dict(row) if row else None
    finally:
        conn.close()


def insert_destination(destination: dict) -> int:
    """
    Inserts a new destination into the database.

    Args:
        destination: Destination dict

    Returns:
        ID of inserted destination
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO destinations (
                    name, country, lat, lon, iata_code,
                    currency_code, language, visa_required,
                    best_time_to_visit, peak_times,
                    beach_score, nightlife_score, city_score,
                    description
                ) VALUES (
                    %(name)s, %(country)s, %(lat)s, %(lon)s, %(iata_code)s,
                    %(currency_code)s, %(language)s, %(visa_required)s,
                    %(best_time_to_visit)s, %(peak_times)s,
                    %(beach_score)s, %(nightlife_score)s, %(city_score)s,
                    %(description)s
                )
                ON CONFLICT DO NOTHING
                RETURNING id
            """, destination)
            conn.commit()
            row = cur.fetchone()
            return row[0] if row else None
    finally:
        conn.close()


def insert_cost_data(destination_id: int, cost_data: dict):
    """
    Inserts or updates cost data for a destination.

    Args:
        destination_id: ID from destinations table
        cost_data:      Dict with avg_meal_cost, cost_of_living_index, safety_index
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO cost_data (
                    destination_id,
                    avg_meal_cost,
                    cost_of_living_index,
                    safety_index
                ) VALUES (%s, %s, %s, %s)
                ON CONFLICT (destination_id)
                DO UPDATE SET
                    avg_meal_cost        = EXCLUDED.avg_meal_cost,
                    cost_of_living_index = EXCLUDED.cost_of_living_index,
                    safety_index         = EXCLUDED.safety_index,
                    last_updated         = CURRENT_TIMESTAMP
            """, (
                destination_id,
                cost_data.get("avg_meal_cost"),
                cost_data.get("cost_of_living_index"),
                cost_data.get("safety_index")
            ))
            conn.commit()
    finally:
        conn.close()


def cache_live_data(destination_id: int, origin_iata: str, live_data: dict):
    """
    Caches live weather, flight and hotel data.
    Prevents hammering APIs on every single request.

    Args:
        destination_id: ID from destinations table
        origin_iata:    Origin airport code e.g. "LGW"
        live_data:      Dict with weather, flight and hotel data
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO live_data (
                    destination_id, origin_iata,
                    avg_temp, humidity, cloudiness,
                    wind_speed, weather_description,
                    flight_cost, flight_duration_hrs,
                    stops, airline,
                    avg_hotel_per_night, hotel_name, hotel_rating
                ) VALUES (
                    %(destination_id)s, %(origin_iata)s,
                    %(avg_temp)s, %(humidity)s, %(cloudiness)s,
                    %(wind_speed)s, %(weather_description)s,
                    %(flight_cost)s, %(flight_duration_hrs)s,
                    %(stops)s, %(airline)s,
                    %(avg_hotel_per_night)s, %(hotel_name)s, %(hotel_rating)s
                )
                ON CONFLICT (destination_id, origin_iata)
                DO UPDATE SET
                    avg_temp             = EXCLUDED.avg_temp,
                    humidity             = EXCLUDED.humidity,
                    cloudiness           = EXCLUDED.cloudiness,
                    wind_speed           = EXCLUDED.wind_speed,
                    weather_description  = EXCLUDED.weather_description,
                    flight_cost          = EXCLUDED.flight_cost,
                    flight_duration_hrs  = EXCLUDED.flight_duration_hrs,
                    stops                = EXCLUDED.stops,
                    airline              = EXCLUDED.airline,
                    avg_hotel_per_night  = EXCLUDED.avg_hotel_per_night,
                    hotel_name           = EXCLUDED.hotel_name,
                    hotel_rating         = EXCLUDED.hotel_rating,
                    last_fetched         = CURRENT_TIMESTAMP
            """, {**live_data, "destination_id": destination_id, "origin_iata": origin_iata})
            conn.commit()
    finally:
        conn.close()