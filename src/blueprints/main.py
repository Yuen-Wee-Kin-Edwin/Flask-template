# src/blueprints/main.py
from flask import Blueprint, render_template, jsonify
from redis.exceptions import ConnectionError
from sqlalchemy import text, inspect
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from src.repositories.redis_repository import RedisRepository

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    from flask import current_app
    redis_service: RedisRepository = current_app.extensions.get("redis_service")
    name = "Edwin"
    redis_service.set_value("user", name)
    person = redis_service.get_value("user")
    return render_template("index.html", person=person)


@main_bp.route("/about")
def about():
    return "<p>About, World!</p>"


@main_bp.route("/health")
def health():
    from flask import current_app
    redis_client = current_app.extensions.get("redis_client")
    db = current_app.extensions.get("db")

    try:
        redis_client.ping()
    except ConnectionError:
        current_app.logger.error("Redis not available")
        return 'Redis not available', 500

    try:
        # Check PostgreSQL connection with a lightweight query.
        db.session.execute(text("SELECT 1"))

        # Inspect to verify if a specific table exists, e.g. 'user'
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        expected_tables = ["user"]

        current_app.logger.info(f"Tables in database: {existing_tables}")
        print(f"Tables in database: {existing_tables}")

        for table_name in expected_tables:
            if table_name not in existing_tables:
                current_app.logger.error(f"PostgreSQL table '{table_name}' missing")
                return f"PostgreSQL table '{table_name}' missing", 500

        # Fetch sample data from user table.
        rows = [dict(row) for row in db.session.execute(text('SELECT * FROM "user" LIMIT 5')).mappings().all()]

        current_app.logger.info(f"Sample data from 'user': {rows}")

        return jsonify({
            "status": "OK",
            "tables": expected_tables,
            "sample_data_user": rows
        }), 200

    except OperationalError:
        current_app.logger.error("PostgreSQL not available")
        return jsonify({"error": "PostgreSQL not available"}), 500

    except SQLAlchemyError as e:
        current_app.logger.error(f"Error querying database: {e}")
        return jsonify({"error": "Database query error"}), 500
