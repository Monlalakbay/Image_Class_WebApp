import os
import sqlite3
import datetime as datetime
from PIL import Image
import io
import numpy as np

#Assuming your .env is in the parent directory of your project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
APP_DIR = os.path.dirname(BASE_DIR)
dotenv_path = os.path.join(APP_DIR, '.env')
UPLOAD_FOLDER = 'photos'

from flask import Flask, render_template, request

app = Flask(__name__, static_folder='static')


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.template_filter('format_number')
def format_number(value):
    if value == 0:
        return "0.000"
    elif abs(value) >= 1:
        return f"{value:.3f}"
    else:
        return f"{value:.3e}"

@app.route('/')
def prediction():
   connection = sqlite3.connect( os.path.join(BASE_DIR, 'database.db'))
   connection.row_factory = sqlite3.Row
   photo_posts = connection.execute( "SELECT * FROM photos_posts WHERE status = true AND date >= date('now', '-3 days') ORDER BY date DESC;" ).fetchall()
   connection.close()

   connection = sqlite3.connect( os.path.join(BASE_DIR, 'database.db'))
   connection.row_factory = sqlite3.Row
   prediction_posts = connection.execute( "SELECT * FROM photos_predictions WHERE photo_foreign_key IN (SELECT id FROM photos_posts WHERE status = true AND date >= date('now', '-3 days')); " ).fetchall()
   connection.close()

   return render_template('posts.html', photo_posts=photo_posts, prediction_posts=prediction_posts)



@app.route('/upload', methods=('GET','POST'))
def upload():
   if request.method == 'POST':
       file = request.files['file']

       if file.filename == '':
           return 'No selected file'

       if file:
           filename = file.filename
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
           file_static_path = os.path.join(BASE_DIR, 'static', file_path)
           file.save(file_static_path)
           status = False
           date = (datetime.datetime.now()).strftime("%Y-%m-%d")

           connection = sqlite3.connect( os.path.join(BASE_DIR, 'database.db'))
           connection.row_factory = sqlite3.Row
           connection.execute(
               'INSERT INTO photos_posts (date, path, status) VALUES (?, ?, ?)',
               (date, file_path.replace('\\','/'), status)
           )
           connection.commit()
           connection.close()

   return render_template('upload.html')

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=5000)
