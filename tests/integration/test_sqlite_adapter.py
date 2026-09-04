from datetime import datetime

from app.adapters.database.sqlite_adapter import SQLiteWeatherRepository
from app.domain.weather import WeatherReading


def test_save_and_find_by_city(tmp_path):
    # Arrange
    database_path = tmp_path / "test.db"
    repository = SQLiteWeatherRepository(str(database_path))

    reading = WeatherReading(
        city="Belagavi",
        temperature=25.0,
        wind_speed=10.0,
        description="Clear sky",
        fetched_at=datetime.now(),
    )

    # Act
    repository.save(reading)
    result = repository.find_by_city("Belagavi")

    # Assert
    assert len(result) == 1
    assert result[0].city == "Belagavi"
    assert result[0].temperature == 25.0
    assert result[0].wind_speed == 10.0
    assert result[0].description == "Clear sky"


def test_find_latest_by_city(tmp_path):
    # Arrange
    database_path = tmp_path / "test.db"
    repository = SQLiteWeatherRepository(str(database_path))

    older_reading = WeatherReading(
        city="Belagavi",
        temperature=22.0,
        wind_speed=7.0,
        description="Cloudy",
        fetched_at=datetime(2026, 9, 5, 10, 0, 0),
    )

    newer_reading = WeatherReading(
        city="Belagavi",
        temperature=25.0,
        wind_speed=10.0,
        description="Clear sky",
        fetched_at=datetime(2026, 9, 5, 11, 0, 0),
    )

    repository.save(older_reading)
    repository.save(newer_reading)

    # Act
    result = repository.find_latest_by_city("Belagavi")

    # Assert
    assert result == newer_reading


def test_find_latest_by_city_when_no_reading_exists(tmp_path):
    # Arrange
    database_path = tmp_path / "test.db"
    repository = SQLiteWeatherRepository(str(database_path))

    # Act
    result = repository.find_latest_by_city("UnknownCity")

    # Assert
    assert result is None