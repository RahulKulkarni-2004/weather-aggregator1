import sqlite3
from datetime import datetime

from app.application.ports import WeatherRepository
from app.domain.weather import WeatherReading


class SQLiteWeatherRepository(WeatherRepository):

    def __init__(self, database_path: str = "weather.db"):
        self.database_path = database_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.database_path)

    def _create_table(self):
        connection = self._get_connection()

        connection.execute("""
            CREATE TABLE IF NOT EXISTS weather_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city TEXT NOT NULL,
                temperature REAL NOT NULL,
                wind_speed REAL NOT NULL,
                description TEXT NOT NULL,
                fetched_at TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    def save(self, reading: WeatherReading) -> WeatherReading:
        connection = self._get_connection()

        connection.execute(
            """
            INSERT INTO weather_readings
            (city, temperature, wind_speed, description, fetched_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                reading.city,
                reading.temperature,
                reading.wind_speed,
                reading.description,
                reading.fetched_at.isoformat(),
            ),
        )

        connection.commit()
        connection.close()

        return reading

    def find_by_city(self, city: str) -> list[WeatherReading]:
        connection = self._get_connection()

        cursor = connection.execute(
            """
            SELECT city, temperature, wind_speed, description, fetched_at
            FROM weather_readings
            WHERE city = ?
            ORDER BY fetched_at DESC
            """,
            (city,),
        )

        rows = cursor.fetchall()
        connection.close()

        return [
            WeatherReading(
                city=row[0],
                temperature=row[1],
                wind_speed=row[2],
                description=row[3],
                fetched_at=datetime.fromisoformat(row[4]),
            )
            for row in rows
        ]

    def find_latest_by_city(self, city: str) -> WeatherReading | None:
        connection = self._get_connection()

        cursor = connection.execute(
            """
            SELECT city, temperature, wind_speed, description, fetched_at
            FROM weather_readings
            WHERE city = ?
            ORDER BY fetched_at DESC
            LIMIT 1
            """,
            (city,),
        )

        row = cursor.fetchone()
        connection.close()

        if row is None:
            return None

        return WeatherReading(
            city=row[0],
            temperature=row[1],
            wind_speed=row[2],
            description=row[3],
            fetched_at=datetime.fromisoformat(row[4]),
        )