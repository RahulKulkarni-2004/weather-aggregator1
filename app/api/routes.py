from flask import Blueprint, jsonify, request

from app.container import weather_service


weather_bp = Blueprint("weather", __name__)


@weather_bp.route("/weather/fetch", methods=["POST"])
def fetch_weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "city is required"}), 400

    try:
        reading = weather_service.fetch_and_save(city)

        return jsonify({
            "city": reading.city,
            "temperature": reading.temperature,
            "wind_speed": reading.wind_speed,
            "description": reading.description,
            "fetched_at": reading.fetched_at.isoformat(),
        })

    except ValueError as error:
        return jsonify({"error": str(error)}), 404

    except Exception:
        return jsonify({"error": "Weather provider is unavailable"}), 503


@weather_bp.route("/weather/<city>", methods=["GET"])
def get_weather_history(city):
    readings = weather_service.get_weather_history(city)

    return jsonify([
        {
            "city": reading.city,
            "temperature": reading.temperature,
            "wind_speed": reading.wind_speed,
            "description": reading.description,
            "fetched_at": reading.fetched_at.isoformat(),
        }
        for reading in readings
    ])


@weather_bp.route("/weather/<city>/latest", methods=["GET"])
def get_latest_weather(city):
    reading = weather_service.get_latest_weather(city)

    if reading is None:
        return jsonify({"error": "No weather data found"}), 404

    return jsonify({
        "city": reading.city,
        "temperature": reading.temperature,
        "wind_speed": reading.wind_speed,
        "description": reading.description,
        "fetched_at": reading.fetched_at.isoformat(),
    })