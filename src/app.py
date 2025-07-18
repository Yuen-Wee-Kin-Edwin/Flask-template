# File: app.py
import logging
import os.path
from urllib.parse import quote_plus

from dotenv import load_dotenv
from flask import Flask
from redis import Redis

from src.entities.webcam_stream import WebcamStream
from src.extensions import db
from src.repositories.redis_repository import RedisRepository


def get_db_password():
    secret_path = "/db/password.txt"
    if os.path.exists(secret_path):
        with open(secret_path) as f:
            return f.read().strip()
    return os.getenv("POSTGRES_PASSWORD")


def load_config():
    env = os.getenv("FLASK_ENV", "development")
    raw_password = get_db_password() if env == "production" else "password"
    # Build DB URI from components
    db_user = os.getenv("POSTGRES_USER")
    db_password = quote_plus(raw_password)
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB")

    # Configure the PostgreSQL database URI
    return {
        "SQLALCHEMY_DATABASE_URI": f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    }


def create_app():
    # Load .env (only in dev)
    load_dotenv()
    app = Flask(__name__)
    app.config.update(load_config())

    db.init_app(app)

    # Connect to Redis server by service name 'redis'
    redis_client = Redis(host='redis', port=6379, decode_responses=True)
    redis_service = RedisRepository(redis_client)

    # Point to a webcam streamer running on Windows host.
    HOST_IP_ADDRESS = "http://host.docker.internal:8080/"
    STREAM_URL = f"{HOST_IP_ADDRESS}stream"
    camera = WebcamStream(stream_url=STREAM_URL)

    # Store these objects in app.extensions for access inside blueprints
    app.extensions["redis_client"] = redis_client
    app.extensions["redis_service"] = redis_service
    app.extensions["redis_service"] = redis_service
    app.extensions["camera"] = camera
    app.extensions["db"] = db

    # Create tables if they do not exist
    with app.app_context():
        try:
            db.create_all()
            app.logger.info("Database tables created or already exist")
            print("Tables created successfully")
        except Exception as e:
            logging.error(f"Error creating tables: {e}")

    # Import blueprints here to avoid circular imports
    from src.blueprints.main import main_bp
    from src.blueprints.video import video_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(video_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0")
