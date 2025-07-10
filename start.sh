#!/usr/bin/env zsh

if [[ "$FLASK_ENV" == "development" ]]; then
  echo "Running in development mode with hot reload..."
  flask run --host=0.0.0.0 --port=8000 --reload
else
  echo "Running in production mode with Gunicorn..."
  gunicorn --bind=0.0.0.0:8000 app:app
fi