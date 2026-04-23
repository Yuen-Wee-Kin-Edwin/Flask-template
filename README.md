# Python Flask template

```zsh
# Setup local development environment.
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

```zsh
# Run/Stop the app
docker compose --profile dev up --build -d
docker compose --profile dev down

# Production
docker compose --profile prod up --build -d
docker compose --profile prod down
```