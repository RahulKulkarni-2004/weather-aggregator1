import responses

from app.app import create_app


def test_fetch_weather():
    app = create_app()
    client = app.test_client()

    with responses.RequestsMock() as mock:
        mock.add(
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

        mock.add(
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

        response = client.post("/weather/fetch?city=Belagavi")

        assert response.status_code == 200

        data = response.get_json()

        assert data["city"] == "belagavi"
        assert data["temperature"] == 25.0
        assert data["wind_speed"] == 10.0
        assert data["description"] == "Clear sky"


def test_fetch_weather_city_not_found():
    app = create_app()
    client = app.test_client()

    with responses.RequestsMock() as mock:
        mock.add(
            responses.GET,
            "https://geocoding-api.open-meteo.com/v1/search",
            json={"results": []},
            status=200,
        )

        response = client.post(
            "/weather/fetch?city=xyzabcnotacity"
        )

        assert response.status_code == 404

        data = response.get_json()

        assert data["error"] == "City not found: xyzabcnotacity"


def test_fetch_weather_missing_city():
    app = create_app()
    client = app.test_client()

    response = client.post("/weather/fetch")

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "city is required"


def test_fetch_weather_provider_failure():
    app = create_app()
    client = app.test_client()

    with responses.RequestsMock() as mock:
        mock.add(
            responses.GET,
            "https://geocoding-api.open-meteo.com/v1/search",
            body=Exception("Open-Meteo unavailable"),
        )

        response = client.post(
            "/weather/fetch?city=Belagavi"
        )

        assert response.status_code == 503

        data = response.get_json()

        assert data["error"] == "Weather provider is unavailable"