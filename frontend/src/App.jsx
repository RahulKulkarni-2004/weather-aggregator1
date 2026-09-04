import { useState } from "react";
import "./App.css";

function App() {
  const [city, setCity] = useState("");
  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fetchWeather = async () => {
    if (!city.trim()) {
      setError("Please enter a city");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const response = await fetch(
        `/weather/fetch?city=${encodeURIComponent(city)}`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to fetch weather");
      }

      const data = await response.json();

      console.log("Weather response:", data);

      setWeather(data);

      const historyResponse = await fetch(
        `/weather/${encodeURIComponent(city)}`
      );

      if (!historyResponse.ok) {
        throw new Error("Failed to fetch weather history");
      }

      const historyData = await historyResponse.json();

      setHistory(historyData);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>Weather Aggregator</h1>

      <div className="search-box">
        <input
          type="text"
          placeholder="Enter city"
          value={city}
          onChange={(e) => setCity(e.target.value)}
        />

        <button onClick={fetchWeather} disabled={loading}>
          {loading ? "Loading..." : "Get Weather"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {weather && (
        <div className="weather-card">
          <h2>{weather.city}</h2>
          <p>Temperature: {weather.temperature} °C</p>
          <p>Wind Speed: {weather.wind_speed} km/h</p>
          <p>Condition: {weather.description}</p>
          <p>Fetched At: {weather.fetched_at}</p>
        </div>
      )}

      {history.length > 0 && (
        <div className="history">
          <h2>Weather History</h2>

          {history.map((reading, index) => (
            <div className="history-item" key={index}>
              <p>
                {reading.temperature} °C — {reading.description} —{" "}
                {reading.fetched_at}
              </p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;