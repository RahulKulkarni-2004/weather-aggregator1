from pathlib import Path

from pact import Pact

from app.adapters.external.open_meteo_adapter import OpenMeteoAdapter


PACT_DIR = Path("pacts")


def test_open_meteo_contract():

    pact = Pact("WeatherAggregator", "OpenMeteo").with_specification("V4")

    # Interaction 1: Geocoding
    (
        pact.upon_receiving("a request to find a city")
        .with_request("GET", "/v1/search")
        .with_query_parameter("name", "Belagavi")
        .with_query_parameter("count", "1")
        .with_query_parameter("language", "en")
        .with_query_parameter("format", "json")
        .will_respond_with(200)
        .with_body(
            {
                "results": [
                    {
                        "latitude": 15.8497,
                        "longitude": 74.4977,
                    }
                ]
            },
            content_type="application/json",
        )
    )

    # Interaction 2: Weather
    (
        pact.upon_receiving("a request to get current weather")
        .with_request("GET", "/v1/forecast")
        .with_query_parameter("latitude", "15.8497")
        .with_query_parameter("longitude", "74.4977")
        .with_query_parameter("current_weather", "true")
        .with_query_parameter("wind_speed_unit", "kmh")
        .will_respond_with(200)
        .with_body(
            {
                "current_weather": {
                    "temperature": 25.0,
                    "windspeed": 10.0,
                    "weathercode": 0,
                }
            },
            content_type="application/json",
        )
    )

    with pact.serve() as server:

        adapter = OpenMeteoAdapter(
            geocoding_base_url=str(server.url),
            weather_base_url=str(server.url),
        )

        reading = adapter.get_weather("Belagavi")

        assert reading.city == "Belagavi"
        assert reading.temperature == 25.0
        assert reading.wind_speed == 10.0
        assert reading.description == "Clear sky"

    PACT_DIR.mkdir(exist_ok=True)
    pact.write_file(PACT_DIR, overwrite=True)