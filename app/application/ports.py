from abc import ABC, abstractmethod

from app.domain.weather import WeatherReading


from abc import ABC, abstractmethod

from app.domain.weather import WeatherReading


class WeatherProvider(ABC):

    @abstractmethod
    def get_weather(self, city: str) -> WeatherReading:
        pass


class WeatherRepository(ABC):

    @abstractmethod
    def save(self, reading: WeatherReading) -> WeatherReading:
        pass

    @abstractmethod
    def find_by_city(self, city: str) -> list[WeatherReading]:
        pass

    @abstractmethod
    def find_latest_by_city(self, city: str) -> WeatherReading | None:
        pass