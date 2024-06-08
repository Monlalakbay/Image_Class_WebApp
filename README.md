# Image classification model for an Online Clothing Shopping Platform

This repository contains an Image classification model that processes images of clothing items and categorizes them into 10 Classes:
0. T-Shirt / Top
1. Trouser
2. Pullover
3. Dress
4. Coat
5. Sandal
6. Shirt
7. Sneaker
8. Bag
9. Ankle boot

This model is deployed as a Restful API, wherein the user can upload photos and see the probabilities per category on a different page.
The system is designed to do batch processing every night.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Author](#author)
7. [Acknowledgments](#acknowledgments)


## Project Overview

This project implements an image classification model which is served via a Flask RESTful API. Batch processing of images is handled by a cron job, and MLflow is utilized to manage the machine learning lifecycle including experimentation, reproducibility, and deployment.The entire application is containerized using Docker.

## Features

- **Flask RESTful API**: Serve the image classification model via HTTP endpoints.
- **Cron Job**: Automate batch processing of images every midnight.
- **MLflow**: Manage and track model versions, parameters, metrics, and artifacts.
- **Docker**: Containerize the application for easy deployment.

## Installation

### Prerequisites

- Docker
- Docker Compose
- Python 3.8+
- pip

### Clone the Repository
```shell
git clone https://github.com/Monlalakbay/Image_Class_WebApp.git
cd image-classification-api
```

### Set Up Virtual Environment
```shell
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```shell
pip install -r requirements.txt
```

### Build Docker Container and run the application
```shell
docker compose up --build
```

## Usage

## API Endpoints

The API will be accessible at ```http://localhost```.

### Post
The User can upload photos( .jpg, .png)  at ```http://localhost/upload```. This photo gets stored and processed overnight.

### Prediction
The User can see the probability the piece of clothing belongs to each category at ```http://localhost```.


## Author

* **Monique Dalida** [GitHub](https://github.com/Monlalakbay)


## Acknowledgments

* Model taken from Tensorflow:https://www.tensorflow.org/tutorials/keras/classification




