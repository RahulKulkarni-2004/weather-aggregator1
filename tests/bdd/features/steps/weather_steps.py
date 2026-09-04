from behave import given, when, then

from app.application.weather_service import WeatherService
from app.domain.weather import WeatherReading


class FakeWeatherProvider:

    def get_weather(self, city):
        return WeatherReading(
            city=city,
            temperature=25.0,
            wind_speed=10.0,
            description="Clear sky",
            fetched_at=__import__("datetime").datetime.now(),
        )


class FakeWeatherRepository:

    def __init__(self):
        self.readings = []

    def save(self, reading):
        self.readings.append(reading)
        return reading

    def find_by_city(self, city):
        return [
            reading
            for reading in self.readings
            if reading.city == city
        ]

    def find_latest_by_city(self, city):
        readings = self.find_by_city(city)
        return readings[-1] if readings else None


def setup_service(context):
    context.repository = FakeWeatherRepository()
    context.provider = FakeWeatherProvider()
    context.service = WeatherService(
        weather_provider=context.provider,
        weather_repository=context.repository,
    )


@given('the weather provider returns weather for "{city}"')
def step_provider_returns_weather(context, city):
    setup_service(context)


@when('I fetch weather for "{city}"')
def step_fetch_weather(context, city):
    context.result = context.service.fetch_and_save(city)


@then('the response should contain temperature "{temperature}"')
def step_check_temperature(context, temperature):
    assert context.result.temperature == float(temperature)


@then('the weather should be saved for "{city}"')
def step_weather_saved(context, city):
    readings = context.repository.find_by_city(city)
    assert len(readings) == 1


@given('weather data exists for "{city}"')
def step_weather_data_exists(context, city):
    setup_service(context)
    context.service.fetch_and_save(city)


@when('I request weather history for "{city}"')
def step_request_history(context, city):
    context.result = context.service.get_weather_history(city)


@then('I should receive weather readings for "{city}"')
def step_check_history(context, city):
    assert len(context.result) > 0
    assert context.result[0].city == city


@when('I request the latest weather for "{city}"')
def step_request_latest(context, city):
    context.result = context.service.get_latest_weather(city)

