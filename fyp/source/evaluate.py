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


def cnn():

    # classes
    classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress',
               'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    images = [f for f in listdir('images') if isfile(join('images', f))]
    scenes = list(map(lambda x: x[:-4], images))

    conn = create_connection('database/fashion.db')
    products = select_product(conn, scenes)

    # load model
    model = load_model('ResNet56v2.h5')

    res = []
    total = 0
    success = 0

    for product in products:
        # load the image if exist
        total += 1
        path = 'images/' + product[2] + '.jpg'
        if os.path.isfile(path) and os.stat(path).st_size > 0:
            img = load_image(path)
            # predict the class
            result = model.predict(img)
            result = np.argmax(result, axis=1)
            for key in result:
                res.append({'actual': product[3], 'predict': classes[key],
                            'result': check_class(product[3], classes[key])})
                if check_class(product[3], classes[key]):
                    success += 1

    print(res, total, success)


def check_class(actual, predict):

    classes = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress',
               'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']

    if actual == 'T-shirt/top' or actual == 'Shirt' or actual == 'Coat':
        return predict == actual or predict == 'Shirt' or predict == 'T-shirt/top' or predict == 'Coat'
    elif actual == 'Sneaker':
        return predict == actual or predict == 'Ankle boot' or predict == 'Sandal'
    else:
        return predict == actual


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


def select_product(conn, scenes):
    # select product record by scene
    sql = "select * from products where scene in ({seq})".format(
        seq=','.join(['?']*len(scenes)))

    cur = conn.cursor()
    cur.execute(sql, scenes)
    rows = cur.fetchall()
    return rows

# 2859 830
# 2859 604.5
# 548 215


# entry point, run the example
evaluate()
