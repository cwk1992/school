import json
import requests
from PIL import Image
import sqlite3
from sqlite3 import Error
import os
import time


def download_image(signature):

    path = 'images/' + signature + '.jpg'
    exist = os.path.isfile(path) and os.stat(path).st_size > 0
    if(not exist):

        prefix = 'http://i.pinimg.com/400x/%s/%s/%s/%s.jpg'
        url = prefix % (signature[0:2], signature[2:4],
                        signature[4:6], signature)

        with open(path, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                print(response)

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
    time.sleep(0.5)


def crop_image(signature, bbox):
    path = 'images/' + signature + '.jpg'

    if os.path.isfile(path) and os.stat(path).st_size > 0:
        im = Image.open(path)
        width, height = im.size

        left = width * bbox[0]
        top = height * bbox[1]
        right = width * bbox[2]
        bottom = height * bbox[3]

        im = im.crop((left, top, right, bottom))
        print(path)
        im.save(path)


def load_fashion_cat():
    # load fashion category data
    with open('clothing_dataset/fashion-cat.json', 'r') as f:
        cat = json.load(f)
    return cat


def load_fashion(cat):
    products = []

    with open('clothing_dataset/fashion.json', 'r') as f:
        i = 1
        line = f.readline()
        while (line and i <= 17488):
            data = json.loads(line)
            # get product, scene, bounding box from fashion data
            product, scene, bbox = data['product'], data['scene'], data['bbox']

            category = cat[product]

            products.append(
                {'product': product, 'scene': scene, 'category': category, 'bbox': bbox})

            # read next line
            line = f.readline()
            print(i)
            i += 1
    return products


def load_fashion_data():

    # load category data
    cat = load_fashion_cat()

    # load fashion data
    products = load_fashion(cat)

    conn = create_connection("database/fashion.db")

    for product in products:
        product, scene, category, bbox = product['product'], product['scene'], product['category'], product['bbox']
        product_id = create_product(conn, (product, scene, category))

        # download image
        # download_image(scene)

    conn.commit()
    conn.close()

    for product in products:
        scene, bbox = product['scene'], product['bbox']

        # crop image according to bounding box
        crop_image(scene, bbox)


def create_connection(db_file):
    # create database connection
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_product(conn, product):
    # insert product record
    sql = ''' INSERT INTO products(product_id,scene,category)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    return cur.lastrowid


load_fashion_data()

# download_image('cdab9160072dd1800038227960ff6467')
# crop_image('cdab9160072dd1800038227960ff6467',
#            [0.434097, 0.859363, 0.560254, 1.0])
