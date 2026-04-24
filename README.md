# Python Flask template

## Installation
Download and install [DBeaver Community Edition](https://dbeaver.io/download/)

```zsh
# Setup local development environment.
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```zsh
# Run/Stop the app
docker compose --profile dev build --no-cache

docker compose --profile dev up --build -d
docker compose --profile dev down
docker compose --profile dev down -v

# Production
docker compose --profile prod up --build -d
docker compose --profile prod down
docker compose --profile prod down -v

docker volume prune -f
```