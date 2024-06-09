#!/bin/bash
set -e

# Activate the Python virtual environment
source /home/${UNAME}/app/venv/bin/activate

# Start Gunicorn by specifying the path to the Flask module
exec gunicorn -w 4 -b 0.0.0.0:8000 webapp.app:app
