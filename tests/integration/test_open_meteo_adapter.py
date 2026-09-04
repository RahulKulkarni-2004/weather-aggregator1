import responses

from app.adapters.external.open_meteo_adapter import OpenMeteoAdapter


@responses.activate
def test_get_weather():
    # Mock geocoding response
    responses.add(
        responses.GET,
        "https://geocoding-api.open-meteo.com/v1/search",
        json={
            "results": [
                {
                    "latitude": 15.8497,
                    "longitude": 74.4977,
                }
            ]
        },
        status=200,
    )

    # Mock weather response
    responses.add(
        responses.GET,
        "https://api.open-meteo.com/v1/forecast",
        json={
            "current_weather": {
                "temperature": 25.0,
                "windspeed": 10.0,
                "weathercode": 0,
            }
        },
        status=200,
    )

    # Act
    adapter = OpenMeteoAdapter()
    result = adapter.get_weather("Belagavi")

    # Assert
    assert result.city == "Belagavi"
    assert result.temperature == 25.0
    assert result.wind_speed == 10.0
    assert result.description == "Clear sky"


@responses.activate
def test_get_weather_city_not_found():
    responses.add(
        responses.GET,
        "https://geocoding-api.open-meteo.com/v1/search",
        json={
            "results": []
        },
        status=200,
    )

    adapter = OpenMeteoAdapter()

    try:
        adapter.get_weather("XYZ")
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "City not found: XYZ"

@responses.activate
def test_get_weather_when_geocoding_api_fails():
    responses.add(
        responses.GET,
        "https://geocoding-api.open-meteo.com/v1/search",
        status=500,
    )

    adapter = OpenMeteoAdapter()

    try:
        adapter.get_weather("Belagavi")
        assert False, "Expected an exception"
    except Exception:
        pass

def test_weather_code_descriptions():
    adapter = OpenMeteoAdapter()

    assert adapter._get_weather_description(0) == "Clear sky"
    assert adapter._get_weather_description(2) == "Partly cloudy"
    assert adapter._get_weather_description(61) == "Slight rain"
    assert adapter._get_weather_description(95) == "Thunderstorm"