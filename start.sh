#!/usr/bin/env zsh

export FLASK_APP=src.app
export PYTHONPATH=/app

echo "Running DB setup..."
python src/db_setup.py

if [[ "$FLASK_ENV" == "development" ]]; then
  echo "Running in development mode with hot reload..."
  flask run --host=0.0.0.0 --port=8000 --reload
else
  echo "Running in production mode with Gunicorn..."
  gunicorn --bind=0.0.0.0:8000 src.app:app
fi