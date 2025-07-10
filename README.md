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
zsh ./setup_env.sh     # if using Zsh
# or
bash ./setup_env.sh    # if using Bash
```

4. Run Flask

```ps
flask --app app:app run
// Hot-reload.
flask --app app:app run --debug
```

3.1 Externally Visible Server

```ps
flask run --host=0.0.0.0
```

## Docker
```zsh
// Production
docker compose up --build -d
docker compose down

// Development
docker compose -f compose.yaml -f docker-compose.override.yaml up --build -d
```