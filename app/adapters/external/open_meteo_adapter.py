import requests
from datetime import datetime

from app.domain.weather import WeatherReading
from app.application.ports import WeatherProvider


class OpenMeteoAdapter(WeatherProvider):

    def __init__(
        self,
        geocoding_base_url="https://geocoding-api.open-meteo.com",
        weather_base_url="https://api.open-meteo.com",
    ):
        self.geocoding_base_url = geocoding_base_url
        self.weather_base_url = weather_base_url

    def get_weather(self, city: str) -> WeatherReading:

        # 1. Find the city's coordinates
        geocoding_url = f"{self.geocoding_base_url}/v1/search"

        geocoding_params = {
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json",
        }

        response = requests.get(
            geocoding_url,
            params=geocoding_params,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        if "results" not in data or not data["results"]:
            raise ValueError(f"City not found: {city}")

        location = data["results"][0]

        latitude = location["latitude"]
        longitude = location["longitude"]

        # 2. Get current weather
        weather_url = f"{self.weather_base_url}/v1/forecast"

        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current_weather": "true",
            "wind_speed_unit": "kmh",
        }

        response = requests.get(
            weather_url,
            params=weather_params,
            timeout=10,
        )

        response.raise_for_status()

        weather_data = response.json()
        current_weather = weather_data["current_weather"]

        # 3. Convert WMO weather code to description
        description = self._get_weather_description(
            current_weather["weathercode"]
        )

        # 4. Create our domain object
        return WeatherReading(
            city=city,
            temperature=current_weather["temperature"],
            wind_speed=current_weather["windspeed"],
            description=description,
            fetched_at=datetime.now(),
        )

    def _get_weather_description(self, weather_code: int) -> str:

        descriptions = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            71: "Slight snow",
            73: "Moderate snow",
            75: "Heavy snow",
            80: "Slight rain showers",
            81: "Moderate rain showers",
            82: "Violent rain showers",
            95: "Thunderstorm",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail",
        }

        return descriptions.get(weather_code, "Unknown")