#!/bin/bash
export FLASK_PORT=5000
export MAP_API_URI="localhost:8080"
export SSL_ENABLED="true"
export DEFAULT_THEME="superhero"

# SSL specific
export CERT_FILE="./certs/cert.pem"
export KEY_FILE="./certs/key.pem"
export MAP_API_PROTOCOL="http://"
. venv/bin/activate
# TODO: add a docker run here
sh maps/start-map-docker.sh
python app.py
