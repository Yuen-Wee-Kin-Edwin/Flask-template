import logging
import os.path

from dotenv import load_dotenv
from flask import Flask, render_template
from redis import Redis
from redis.exceptions import ConnectionError
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError
from urllib.parse import quote_plus

from src.extensions import db
from src.repositories.redis_repository import RedisRepository

# Load .env (only in dev)
load_dotenv()
app = Flask(__name__)
# Connect to Redis server by service name 'redis'
redis_client = Redis(host='redis', port=6379, decode_responses=True)
redis_service = RedisRepository(redis_client)

def get_db_password():
    secret_path = "/db/password.txt"
    if os.path.exists(secret_path):
        with open(secret_path) as f:
            return f.read().strip()
    return os.getenv("POSTGRES_PASSWORD")

# Build DB URI from components
db_user = os.getenv("POSTGRES_USER")
db_password = quote_plus(get_db_password())
db_host = os.getenv("POSTGRES_HOST", "localhost")
db_port = os.getenv("POSTGRES_PORT", "5432")
db_name = os.getenv("POSTGRES_DB")

# Configure the PostgreSQL database URI
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

# Create tables if they do not exist
with app.app_context():
    try:
        db.create_all()
        app.logger.info("Database tables created or already exist")
        print("Tables created successfully")
    except Exception as e:
        logging.error(f"Error creating tables: {e}")

@app.route("/")
def index():
    name = "Edwin"
    redis_service.set_value("user", name)
    person = redis_service.get_value("user")
    return render_template("index.html", person=person)

@app.route("/about")
def about():
    return "<p>About, World!</p>"

@app.route("/health")
def health():
    try:
        redis_client.ping()
    except ConnectionError:
        logging.error("Redis not available")
        return 'Redis not available', 500

    try:
        # Check PostgreSQL connection with a lightweight query.
        db.session.execute(text("SELECT 1"))

        # Inspect to verify if a specific table exists, e.g. 'user'
        inspector = inspect(db.engine)
        existing_tables  = inspector.get_table_names()

        expected_tables = ["user"]

        logging.info(f"Tables in database: {existing_tables }")
        print(f"Tables in database: {existing_tables }")

        for table_name in expected_tables:
            if table_name not in existing_tables:
                logging.error(f"PostgreSQL table '{table_name}' missing")
                return f"PostgreSQL table '{table_name}' missing", 500

        # If all tables are present
        return f"All expected tables present: {existing_tables}", 200

    except OperationalError:
        logging.error("PostgreSQL not available")
        return "PostgreSQL not available", 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")