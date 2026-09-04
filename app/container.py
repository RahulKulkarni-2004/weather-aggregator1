from app.application.weather_service import WeatherService
from app.adapters.external.open_meteo_adapter import OpenMeteoAdapter
from app.adapters.database.sqlite_adapter import SQLiteWeatherRepository


weather_provider = OpenMeteoAdapter()
weather_repository = SQLiteWeatherRepository()

weather_service = WeatherService(
    weather_provider=weather_provider,
    weather_repository=weather_repository,
)