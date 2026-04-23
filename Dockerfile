FROM python:3.13-slim AS base

WORKDIR /app

# Install essential system dependencies.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/

# --- Development Stage ---
FROM base AS development
# Enable Flask debug for hot-reloading and verbose error logging.
ENV FLASK_DEBUG=1
EXPOSE 5000
CMD [ "flask" , "run" , "--host=0.0.0.0" ]

# --- Production Stage ---
FROM base AS production
RUN pip install gunicorn
# Disable debug mode for security.
ENV FLASK_DEBUG=0
EXPOSE 8000
CMD [ "gunicorn", "--bind", "0.0.0.0:8000", "src.app:create_app()" ]