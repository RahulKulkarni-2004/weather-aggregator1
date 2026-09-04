from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/v1/search", methods=["GET"])
def geocoding():
    return jsonify({
        "results": [
            {
                "latitude": 15.8497,
                "longitude": 74.4977,
            }
        ]
    })


@app.route("/v1/forecast", methods=["GET"])
def weather():
    return jsonify({
        "current_weather": {
            "temperature": 25.0,
            "windspeed": 10.0,
            "weathercode": 0,
        }
    })


if __name__ == "__main__":
    app.run(port=5001)