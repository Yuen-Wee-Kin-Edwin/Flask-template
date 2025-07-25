# Flask-template

1. Setup python virtual environment.

**Windows**

```ps
// Install virtualenv package
pip install virtualenv

// Create a virtual environment.
py -3 -m venv .venv

// Activate virtual environment
.venv\Scripts\activate

// Install required packages
pip install -r requirements.txt

// Deactivate virtual environment
deactivate
```

**Linux (Ubuntu)**

```zsh
sudo apt update
sudo apt install python3 python3-venv

// Create a virtual environment.
python3 -m venv .venv

// Activate the virtual environment.
source .venv/bin/activate

// Deactivate virtual environment
deactivate
```

2. Install dependencies

```zsh
pip install -r requirements.txt
```

3. Setup environment files

Run the script to initialise `.env` files from the example files:

```bash
zsh ./scripts/setup_env.sh                                        # if using Zsh
# or
bash ./scripts/setup_env.sh                                       # if using Bash
# or
powershell -ExecutionPolicy Bypass -File .\scripts\setup_env.ps1  # if using PowerShell
```

4. Run Flask app only

```ps
$env:USE_DATABASE="false"; $env:USE_REDIS="false"; flask --app src.app:app run
// Hot-reload.
$env:USE_DATABASE="false"; $env:USE_REDIS="false"; flask --app src.app:app run --reload
// Externally Visible Server
$env:FLASK_DEBUG="1"; $env:USE_DATABASE="false"; $env:USE_REDIS="false"; flask --app src.app:app run --host=0.0.0.0 --reload
```

## Database (PostgreSQL)

Setup

1. Create a password file:

Windows

```zsh
New-Item -ItemType Directory -Force -Path .\db
'your_secure_password' > .\db\password.txt

```

Linux

```zsh
mkdir -p db
echo 'your_secure_password' > db/password.txt
chmod 600 db/password.txt
```

## Docker

```zsh
// Development
./scripts/dev_up.sh
./scripts/dev_wipe.sh
docker compose down
psql -h localhost -p 5432 -U postgres -d db
docker volume rm db-dev

// Production
docker compose -f compose.yaml up --build -d
./scripts/prod_up.sh
./scripts/prod_wipe.sh
docker compose down
docker volume rm db-prod
```

### Docker Health Check

```zsh
curl -k -i https://localhost/health
```

## SSL

Linux (Created Self-Signed Cert)

```zsh
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:4096 \
  -keyout certs/selfsigned.key \
  -out certs/selfsigned.crt \
  -subj "/CN=localhost"
```
