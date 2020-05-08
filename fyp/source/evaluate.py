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
    ids = list(map(lambda x: x[:-4], images))

    conn = create_connection('database/fashion.db')
    products = select_product(conn, ids)

    # load model
    model = load_model('ResNet56v2.h5')

    res = []
    total = 0
    success = 0

    for product in products:
        # load the image if exist
        total += 1
        path = 'images/' + str(product[0]) + '.jpg'
        if os.path.isfile(path) and os.stat(path).st_size > 0:
            img = load_image(path)
            # predict the class
            result = model.predict(img)
            result = np.argmax(result, axis=1)
            for key in result:
                res.append({'id': product[0], 'actual': product[3], 'predict': classes[key],
                            'result': check_class(product[3], classes[key])})
                success += check_class(product[3], classes[key])

    print(res, total, success)


def check_class(actual, predict):
    if actual == 'T-shirt/top':
        return int(predict == 'T-shirt/top' or predict == 'Pullover' or predict == 'Shirt')
    elif actual == 'Sneaker':
        return int(predict == 'Sneaker' or predict == 'Sandal' or predict == 'Ankle boot')
    elif actual == 'Coat' and (predict == 'T-shirt/top' or predict == 'Pullover' or predict == 'Shirt'):
        return 1
    else:
        return int(predict == actual)


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

# 2859 830
# 2859 604.5
# 548 215
# 2862 716.0


# entry point, run the example
evaluate()
