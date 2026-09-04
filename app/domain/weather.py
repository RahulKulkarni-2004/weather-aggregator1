from dataclasses import dataclass
from datetime import datetime


@dataclass
class WeatherReading:
    city: str
    temperature: float
    wind_speed: float
    description: str
    fetched_at: datetime