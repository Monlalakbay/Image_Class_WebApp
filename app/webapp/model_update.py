import os
import sqlite3
import pandas as pd

import numpy as np
import tensorflow as tf
import mlflow
from PIL import Image

def preprocess_image(image_path):
    # Open the image using Pillow
    image = Image.open(image_path)
    
    # Resize the image to match the input shape of the model (28x28 pixels)
    resized_image = image.resize((28, 28))
    
    # Convert the image to grayscale
    gray_image = resized_image.convert("L")
    
    # Normalize pixel values to the range [0, 1]
    normalized_image = np.array(gray_image) / 255.0
    
    # Reshape the image to match the input shape expected by the model
    preprocessed_image = np.expand_dims(normalized_image, axis=0)
    
    return preprocessed_image

def process_images(BASE_DIR, idx, image_path):
    # Load Model
    loaded_model = mlflow.tensorflow.load_model(os.path.join(BASE_DIR, "fashion_mnist_model"))
    
    # Preprocess the new image
    input_image = preprocess_image(image_path)

    # Perform inference using the loaded model
    predictions = loaded_model.predict(input_image)

    # Establish connection to the SQLite database
    database_path = os.path.join(BASE_DIR, 'database.db')
    connection = sqlite3.connect(database_path)
    # connection = sqlite3.connect( os.path.join(BASE_DIR, 'database.db'))
    connection.row_factory = sqlite3.Row
    
    result = (idx,) + tuple(predictions.flatten())
    
    # Insert prediction probabilities into the database
    connection.execute(
        'INSERT INTO photos_predictions (photo_foreign_key, top_prediction, trouser_prediction, pullover_prediction, dress_prediction, coat_prediction, sandal_prediction, shirt_prediction, sneaker_prediction, bag_prediction, ankle_boot_prediction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (int(result[0]), float(100 * result[1]), float(100 * result[2]), float(100 * result[3]), float(100 * result[4]), float(100 * result[5]), float(100 * result[6]), float(100 * result[7]), float(100 * result[8]), float(100 * result[9]), float(100 * result[10]))
    )
    connection.commit()
    connection.close()
    
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    
    # Create a cursor object to interact with the database
    cursor = conn.cursor()
    
    # Define the SQL query to update the status to True for the row with id = 1
    sql_query = """
                UPDATE photos_posts
                SET status = ?
                WHERE id = ?
                """
    
    # Execute the SQL query with the appropriate parameters
    cursor.execute(sql_query, (True, idx))
    
    # Commit the transaction to make the changes permanent
    conn.commit()
    
    # Close the cursor and connection
    cursor.close()
    conn.close()

# Specify the base directory explicitly
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Establishing connection to the SQLite database
database_path = os.path.join(BASE_DIR, 'database.db')

# Establishing connection to the SQLite database
connection = sqlite3.connect(database_path )
connection.row_factory = sqlite3.Row

# Executing the SQL query to fetch photo_posts
photo_posts = connection.execute( "SELECT * FROM photos_posts WHERE status = false;" ).fetchall()

# Closing the connection
connection.close()

# Converting the fetched data into a Pandas DataFrame
photo_posts_df = pd.DataFrame([dict(row) for row in photo_posts])


for index, row in photo_posts_df.iterrows():
    file_path = os.path.join(BASE_DIR, 'static', row['path'])
    process_images(BASE_DIR, row['id'], file_path)
    print(file_path)
#%%
