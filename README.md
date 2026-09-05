# Weather Aggregator

A full-stack weather aggregation application built with **Python, Flask, React, SQLite, and Open-Meteo**.

The application fetches current weather information for a city, persists each reading locally, and exposes REST APIs to retrieve historical and latest readings.

The backend follows **Hexagonal Architecture (Ports and Adapters)**, keeping the application core independent from external APIs, databases, HTTP frameworks, and infrastructure.

---

## Features

* Fetch current weather for a city
* Resolve city coordinates using Open-Meteo Geocoding
* Retrieve current weather using Open-Meteo Forecast API
* Persist weather readings in SQLite
* Retrieve weather history for a city
* Retrieve the latest stored reading
* Human-readable WMO weather descriptions
* Flask REST API
* React frontend using Vite
* Hexagonal Architecture (Ports and Adapters)
* Unit, integration, component, contract, and BDD tests
* React component testing
* Error handling for invalid requests, unknown cities, and provider failures

---

## Architecture

The backend follows **Hexagonal Architecture (Ports and Adapters)**.

```text
                          +----------------------+
                          |      React UI        |
                          +----------+-----------+
                                     |
                                     | HTTP
                                     v
                          +----------------------+
                          |     Flask API        |
                          +----------+-----------+
                                     |
                                     v
                     +-------------------------------+
                     |        WeatherService         |
                     |        Application Core       |
                     +---------------+---------------+
                                     |
                      +--------------+--------------+
                      |                             |
                      v                             v
              WeatherProvider              WeatherRepository
                    Port                         Port
                      |                             |
                      v                             v
              OpenMeteoAdapter              SQLiteAdapter
                      |                             |
                      v                             v
               Open-Meteo API                  weather.db
```

### Dependency Direction

The application core depends on **ports (interfaces)** rather than concrete infrastructure.

```text
WeatherService
      |
      +---- WeatherProvider
      |
      +---- WeatherRepository
             |
             +---- OpenMeteoAdapter
             +---- SQLiteAdapter
```

This allows external systems to be replaced without changing the core application logic.

---

## Project Structure

```text
weather-aggregator/
|
+-- app/
|   +-- domain/
|   +-- application/
|   +-- adapters/
|   |   +-- external/
|   |   +-- database/
|   +-- api/
|   +-- container.py
|   +-- app.py
|
+-- tests/
|   +-- unit/
|   +-- integration/
|   +-- component/
|   +-- contract/
|   +-- bdd/
|
+-- frontend/
|   +-- src/
|   +-- package.json
|   +-- vite.config.js
|
+-- requirements.txt
+-- .gitignore
+-- README.md
```

---

## Technology Stack

### Backend

* Python
* Flask
* Requests
* SQLite

### Frontend

* React
* Vite
* JavaScript

### Testing

* Pytest
* Responses
* Pact
* Behave
* React Testing Library
* Vitest

---

## Weather Data Flow

When a user requests weather for a city:

1. React sends a request to the Flask API.
2. Flask passes the request to `WeatherService`.
3. `WeatherService` uses the `WeatherProvider` port.
4. `OpenMeteoAdapter` resolves the city coordinates.
5. `OpenMeteoAdapter` requests current weather data.
6. The weather data is converted into a domain `WeatherReading`.
7. `WeatherService` uses the `WeatherRepository` port.
8. `SQLiteWeatherRepository` stores the reading.
9. The saved reading is returned to the API.
10. Flask returns the result as JSON.
11. React displays the weather and stored history.

---

## API Endpoints

| Method | Endpoint                     | Description                    |
| ------ | ---------------------------- | ------------------------------ |
| POST   | `/weather/fetch?city={city}` | Fetch and save current weather |
| GET    | `/weather/{city}`            | Get weather history            |
| GET    | `/weather/{city}/latest`     | Get latest weather reading     |

### Example

```text
POST /weather/fetch?city=Belagavi
```

Response:

```json
{
  "city": "Belagavi",
  "temperature": 25.0,
  "wind_speed": 10.0,
  "description": "Clear sky",
  "fetched_at": "2026-09-05T12:00:00"
}
```

---

## Weather Data

Each stored reading contains:

* City
* Temperature in Celsius
* Wind speed in km/h
* Human-readable weather description
* Fetch timestamp

Weather descriptions are generated from the **WMO weather codes** returned by Open-Meteo.

---

## External API

The application uses **Open-Meteo** for:

1. City geocoding
2. Current weather data

No API key is required.

---

## Database

SQLite is used as the persistence layer.

The database is created automatically as:

```text
weather.db
```

The database stores every successful weather fetch, allowing historical readings to be retrieved.

---

## Testing Strategy

The project contains multiple levels of automated testing.

### Unit Tests

Test `WeatherService` independently using fake or mocked ports.

Covered cases include:

* Successful weather fetch and save
* External provider failure
* City not found

### Integration Tests

Test the SQLite repository against a real SQLite database without mocking the database.

Also test the Open-Meteo adapter against stubbed HTTP responses.

### Component Tests

Test the Flask REST API together with the application and adapter layers while stubbing external HTTP calls.

### Contract Tests

Pact is used to define and verify the contract between:

```text
Weather Aggregator → Open-Meteo
```

A local provider stub is used for provider verification.

### BDD Tests

Behave scenarios cover:

* Fetching and saving weather
* Retrieving weather history
* Retrieving the latest reading

### Frontend Tests

React Testing Library and Vitest are used to verify important UI elements and interactions.

---

## Current Test Status

Backend:

```text
18 pytest tests passed
```

BDD:

```text
3 scenarios passed
10 steps passed
```

Frontend:

```text
1 React component test passed
```

Frontend linting also passes successfully.

---

## Running the Backend

Activate the virtual environment and run:

```powershell
python -m app.app
```

The backend runs on:

```text
http://127.0.0.1:5000
```

---

## Running Backend Tests

From the project root:

```powershell
$env:PYTHONPATH="."
pytest -q
```

---

## Running BDD Tests

```powershell
behave tests/bdd/features
```

---

## Running the Frontend

From the project root:

```powershell
cd frontend
npm run dev
```

The React application uses the Vite development proxy to communicate with the Flask backend.

---

## Running Frontend Tests

```powershell
cd frontend
npm test -- --run
```

---

## Frontend Lint

```powershell
cd frontend
npm run lint
```

---

## Design Principles

* Domain logic is independent of Flask, SQLite, Requests, and external APIs.
* Application services depend on ports rather than concrete infrastructure.
* External systems are accessed through adapters.
* Dependencies point toward the application core.
* External APIs are stubbed during automated tests.
* Infrastructure details can be replaced without changing the core business logic.

---

## Future Improvements

Possible future improvements include:

* More specific custom exception handling
* Database migrations
* Additional frontend tests
* Production deployment configuration
* Structured logging
* Improved observability
* Authentication and authorization
* More weather data and forecast support

---

## License

This project was created as a technical assignment given to me on 04/09/2026 by Nokia.

Thank you, 
Kind regards,

Rahul Kulkarni.