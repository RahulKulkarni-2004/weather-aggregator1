from flask import Flask

from app.api.routes import weather_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(weather_bp)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)