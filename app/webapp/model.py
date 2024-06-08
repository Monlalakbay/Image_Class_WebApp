import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# TensorFlow and tf.keras
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist

# Helper libraries
import mlflow
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
mlflow.autolog() #log metrics, parameters, and models without the need for explicit log statements


##Import Dataset
# Fashion MNIST dataset which contains 70,000 grayscale images in 10 categories at low resolution (28 by 28 pixels)
# 60,000 images are used to train the network and 10,000 images to evaluate
# Load Fashion MNIST dataset
(train_images, train_labels), (test_images, test_labels) = fashion_mnist.load_data()
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

##Preprocess Data
# Scale
train_images = train_images / 255.0
test_images = test_images / 255.0


##Build the model
#Set up layers : The basic building block of a neural network is the layer. Layers extract representations from the data fed into them.
model = tf.keras.Sequential([
    tf.keras.layers.Flatten(input_shape=(28, 28)), # transforms the format of the images from a two-dimensional array (to a one-dimensional array
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

# Compile the model
model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(),
              metrics=['accuracy'])

# =============================================================================
# ## Start MLflow run
# # New runs are launched under this experiment
# with mlflow.start_run() as run:
#     # Log parameters
#     mlflow.log_param("epochs", 10)
# 
# ## Train the model
# model.fit(train_images, train_labels, epochs=10)
# 
# ## Evaluate Accuracy
# test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
# mlflow.log_metric("test_loss", test_loss)
# mlflow.log_metric("test_accuracy", test_acc)
# 
# # Log model
# mlflow.tensorflow.log_model(model, "fashion_mnist_model")
# 
# # Print test accuracy
# print('\nTest accuracy:', test_acc)
# 
# # Save the model
# mlflow.tensorflow.save_model("imageclass_fashion_mnist_model", BASE_DIR)
# =============================================================================


## Start MLflow run
# New runs are launched under this experiment
with mlflow.start_run() as run:
    # Log parameters
    mlflow.log_param("epochs", 10)

    ## Train the model
    model.fit(train_images, train_labels, epochs=10)

    ## Evaluate Accuracy
    test_loss, test_acc = model.evaluate(test_images,  test_labels, verbose=2)
    mlflow.log_metric("test_loss", test_loss)
    mlflow.log_metric("test_accuracy", test_acc)

    # Log model
    mlflow.tensorflow.log_model(model, "fashion_mnist_model")


    # Save model
    mlflow.tensorflow.save_model(model, os.path.join(BASE_DIR, "fashion_mnist_model"))

# Print test accuracy
print('\nTest accuracy:', test_acc)