from app.application.ports import WeatherProvider, WeatherRepository
from app.domain.weather import WeatherReading


class WeatherService:

    def __init__(
        self,
        weather_provider: WeatherProvider,
        weather_repository: WeatherRepository,
    ):
        self.weather_provider = weather_provider
        self.weather_repository = weather_repository

    def fetch_and_save(self, city: str) -> WeatherReading:
        reading = self.weather_provider.get_weather(city)
        return self.weather_repository.save(reading)

    def get_weather_history(self, city: str) -> list[WeatherReading]:
        return self.weather_repository.find_by_city(city)

    def get_latest_weather(self, city: str) -> WeatherReading | None:
        return self.weather_repository.find_latest_by_city(city)