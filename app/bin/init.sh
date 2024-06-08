#!/bin/bash

# Attiva l'ambiente virtuale Python
source /home/${UNAME}/app/venv/bin/activate

# Execute the Python script
python /home/${UNAME}/app/webapp/init_db.py