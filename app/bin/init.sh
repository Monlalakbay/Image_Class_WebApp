#!/bin/bash

#  Activate the Python virtual environment
source /home/${UNAME}/app/venv/bin/activate

# Execute the Python script
python /home/${UNAME}/app/webapp/init_db.py
