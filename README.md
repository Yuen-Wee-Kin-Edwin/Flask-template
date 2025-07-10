# Flask-template

1. Setup python virtual environment.

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

2. Run Flask

```ps
flask --app app:app run
// Hot-reload.
flask --app app:app run --debug
```

2.1 Externally Visible Server

```ps
flask run --host=0.0.0.0
```