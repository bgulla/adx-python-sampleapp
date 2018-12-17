#!/bin/bash
export FLASK_PORT=5000
export MAP_API_URI="localhost:8080"
export SSL_ENABLED="false"
export DEFAULT_THEME="superhero"

. venv/bin/activate
# TODO: add a docker run here
python app.py
