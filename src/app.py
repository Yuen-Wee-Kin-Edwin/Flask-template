from flask import Flask, render_template
from redis import Redis
from redis.exceptions import ConnectionError

from src.repositories.redis_repository import RedisRepository

app = Flask(__name__)
# Connect to Redis server by service name 'redis'
redis_client = Redis(host='redis', port=6379, decode_responses=True)
redis_service = RedisRepository(redis_client)

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
        return '', 200
    except ConnectionError:
        return 'Redis not available', 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")