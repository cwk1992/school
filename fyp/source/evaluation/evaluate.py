# make a prediction for a new image.
import numpy as np
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from sklearn.metrics import classification_report
import os
from os import listdir
from os.path import isfile, join
import sqlite3
from sqlite3 import Error
import json
import random

# load and prepare the image


def load_image(filename):
    # load the image
    img = load_img(filename, grayscale=True, target_size=(28, 28))
    # convert to array
    img = img_to_array(img)
    # reshape into a single sample with 1 channel
    img = img.reshape(1, 28, 28, 1)
    # prepare pixel data
    img = img.astype('float32')
    img = img / 255.0
    return img

# load an image and predict the class


def cnn(threshold=0.6):

    # classes
    classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress',
               'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    images = [f for f in listdir('../images') if isfile(join('../images', f))]
    # ids = list(map(lambda x: x[:-4], images))
    ids = [3693]

    conn = create_connection('../database/fashion.db')
    products = select_product(conn, ids)

    # load model
    model = load_model('../image_recognition/saved_model/ResNet56v2.h5')

    res = {'T-shirt/top': [], 'Trouser': [], 'Pullover': [], 'Dress': [],
           'Coat': [], 'Sandal': [], 'Shirt': [], 'Sneaker': [], 'Bag': [], 'Ankle boot': []}
    calres = {'T-shirt/top': [0, 0], 'Trouser': [0, 0], 'Pullover': [0, 0], 'Dress': [0, 0],
              'Coat': [0, 0], 'Sandal': [0, 0], 'Shirt': [0, 0], 'Sneaker': [0, 0], 'Bag': [0, 0], 'Ankle boot': [0, 0]}

    for product in products:
        # load the image if exist
        actual_class = ran_class(product[3])
        path = '../images/' + str(product[0]) + '_1.jpg'
        # if os.path.isfile(path) and os.stat(path).st_size > 0:
        img = load_image(path)
        # predict the class
        proba = model.predict(img)
        result = np.argmax(proba, axis=1)
        p = proba[0][result][0]
        # if p > threshold:
        calres[actual_class][0] += 1
        for key in result:
            res[actual_class].append({'id': product[0], 'actual': actual_class, 'proba': str(p), 'predict': classes[key],
                                      'result': check_class(product[3], classes[key])})
            res[actual_class].append(proba.tolist())

            calres[actual_class
                   ][1] += check_class(product[3], classes[key])

        actual_class = ran_class(product[3])
        path = '../images/' + str(product[0]) + '_2.jpg'
        # if os.path.isfile(path) and os.stat(path).st_size > 0:
        img = load_image(path)
        # predict the class
        proba = model.predict(img)
        result = np.argmax(proba, axis=1)
        p = proba[0][result][0]
        # if p > threshold:
        calres[actual_class][0] += 1
        for key in result:
            res[actual_class].append({'id': product[0], 'actual': actual_class, 'proba': str(p), 'predict': classes[key],
                                      'result': check_class(product[3], classes[key])})

            res[actual_class].append(proba.tolist())
            calres[actual_class
                   ][1] += check_class(product[3], classes[key])

    with open('res.json', 'w') as f:
        json.dump(res, f)

    with open('calres.json', 'w') as f:
        json.dump(calres, f)


def check_class(actual, predict):
    return int(predict in actual.split('|'))


def ran_class(actual):
    return random.choice(actual.split('|'))


def evaluate():
    cnn()


def create_connection(db_file):
    # create database connection
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_product(conn, ids):
    # select product record by scene
    sql = "select * from products where id in ({seq})".format(
        seq=','.join(['?']*len(ids)))

    cur = conn.cursor()
    cur.execute(sql, ids)
    rows = cur.fetchall()
    return rows


# entry point, run the example
evaluate()
