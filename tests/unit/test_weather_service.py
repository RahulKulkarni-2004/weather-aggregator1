from datetime import datetime
from unittest.mock import Mock

from app.application.weather_service import WeatherService
from app.domain.weather import WeatherReading


def test_fetch_and_save_weather():
    # Arrange
    provider = Mock()
    repository = Mock()

    reading = WeatherReading(
        city="Belagavi",
        temperature=25.0,
        wind_speed=10.0,
        description="Clear sky",
        fetched_at=datetime.now(),
    )

    provider.get_weather.return_value = reading
    repository.save.return_value = reading

    service = WeatherService(provider, repository)

    # Act
    result = service.fetch_and_save("Belagavi")

    # Assert
    assert result == reading
    provider.get_weather.assert_called_once_with("Belagavi")
    repository.save.assert_called_once_with(reading)



def test_fetch_and_save_when_provider_fails():
    # Arrange
    provider = Mock()
    repository = Mock()

    provider.get_weather.side_effect = Exception("Open-Meteo is unavailable")

    service = WeatherService(provider, repository)

    # Act & Assert
    try:
        service.fetch_and_save("Belagavi")
        assert False, "Expected an exception"
    except Exception as error:
        assert str(error) == "Open-Meteo is unavailable"

    repository.save.assert_not_called()   


def test_get_weather_history():
    # Arrange
    provider = Mock()
    repository = Mock()

    readings = [
        WeatherReading(
            city="Belagavi",
            temperature=25.0,
            wind_speed=10.0,
            description="Clear sky",
            fetched_at=datetime.now(),
        )
    ]

    repository.find_by_city.return_value = readings

    service = WeatherService(provider, repository)

    # Act
    result = service.get_weather_history("Belagavi")

    # Assert
    assert result == readings
    repository.find_by_city.assert_called_once_with("Belagavi")


def test_get_latest_weather():
    # Arrange
    provider = Mock()
    repository = Mock()

    reading = WeatherReading(
        city="Belagavi",
        temperature=24.0,
        wind_speed=8.0,
        description="Partly cloudy",
        fetched_at=datetime.now(),
    )

    repository.find_latest_by_city.return_value = reading

    service = WeatherService(provider, repository)

    # Act
    result = service.get_latest_weather("Belagavi")

    # Assert
    assert result == reading
    repository.find_latest_by_city.assert_called_once_with("Belagavi")



def test_fetch_and_save_when_city_not_found():
    # Arrange
    provider = Mock()
    repository = Mock()

    provider.get_weather.side_effect = ValueError("City not found: XYZ")

    service = WeatherService(provider, repository)

    # Act & Assert
    try:
        service.fetch_and_save("XYZ")
        assert False, "Expected an exception"
    except ValueError as error:
        assert str(error) == "City not found: XYZ"

    repository.save.assert_not_called()