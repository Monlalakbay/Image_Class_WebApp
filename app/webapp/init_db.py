import sqlite3
import os
import shutil
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Establishing connection to the SQLite database
database_path = os.path.join(BASE_DIR, 'database.db')

if ( os.path.exists(database_path) ):
    os.remove(database_path)

# Clear the photos directory
photo_path = os.path.join(BASE_DIR, 'static', 'photos')
entries = os.listdir(photo_path)
# Loop through the entries
for entry in entries:
    full_path = os.path.join(photo_path, entry)
    os.remove(full_path)


# Remove the model directories if they exist
model_1_path = os.path.join(BASE_DIR, 'fashion_mnist_model')
if ( os.path.exists(model_1_path) ):
    shutil.rmtree(model_1_path)


model_2_path = os.path.join(BASE_DIR, 'mlruns')
if ( os.path.exists(model_2_path) ):
    shutil.rmtree(model_2_path)

# Run the model script
subprocess.run(["python", os.path.join(BASE_DIR, 'model.py')])


# Connect to the SQLite database and execute the SQL script
sql_file_path = os.path.join(BASE_DIR, 'create_database.sql')


connection = sqlite3.connect(database_path)

with open(sql_file_path) as f:
    connection.executescript(f. read())
connection.commit()
connection.close()