import json
import requests
from PIL import Image
import sqlite3
from sqlite3 import Error
import os
import time
import itertools
import random


def download_image(signature, id):

    path = 'images/' + str(id) + '.jpg'
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


def crop_image(id, bbox):
    path = 'images/' + str(id) + '.jpg'

    if os.path.isfile(path) and os.stat(path).st_size > 0:
        im = Image.open(path)
        width, height = im.size

        left = width * bbox[0]
        top = height * bbox[1]
        right = width * bbox[2]
        bottom = height * bbox[3]

        im = im.crop((left, top, right, bottom))
        im.save(path)


def load_fashion_cat():
    # load fashion category data
    with open('clothing_dataset/fashion-cat.json', 'r') as f:
        cat = json.load(f)
    return cat


def load_fashion(cat, threshold=0.4):
    products = []

    ref = {'Apparel & Accessories|Clothing|Shirts & Tops': 'T-shirt/top|Pullover|Shirt',
           'Apparel & Accessories|Clothing|Pants': 'Trouser',
           'Apparel & Accessories|Handbags, Wallets & Cases': 'Bag',
           'Apparel & Accessories|Clothing|Skirts': 'Dress',
           'Apparel & Accessories|Shoes': 'Sandal|Sneaker|Ankle boot',
           'Apparel & Accessories|Clothing|Shorts': 'Trouser',
           'Apparel & Accessories|Clothing|Outerwear|Coats & Jackets': 'Coat'}

    with open('clothing_dataset/fashion.json', 'r') as f:
        line = f.readline()
        while (line):
            data = json.loads(line)
            # get product, scene, bounding box from fashion data
            product, scene, bbox = data['product'], data['scene'], data['bbox']

            category = cat[product]

            if (category in ref and abs(bbox[0] - bbox[2]) > threshold and (abs(bbox[1] - bbox[3]) > threshold)):
                products.append(
                    {'product': product, 'scene': scene, 'category': ref[category], 'bbox': bbox})

            # read next line
            line = f.readline()

    random.shuffle(products)
    return products


def delete_image(dir='images'):
    filelist = [f for f in os.listdir(dir) if f.endswith(".jpg")]
    for f in filelist:
        os.remove(os.path.join(dir, f))


def key_f(x): return x['category']


def load_fashion_data():

    conn = create_connection("../database/fashion.db")

    # load category data
    # cat = load_fashion_cat()

    # load fashion data
    # products = load_fashion(cat)
    products = select_product(conn)

    for product in products:
        colors = list(product[8:])
        colors.sort()
        update_product(conn, product[0], colors)

    # # reset product table
    # reset_product(conn)

    # res = {'T-shirt/top|Pullover|Shirt': [],
    #        'Trouser': [],
    #        'Bag': [],
    #        'Dress': [],
    #        'Sandal|Sneaker|Ankle boot': [],
    #        'Trouser': [],
    #        'Coat': []}

    # for product in products:
    #     # res[product['category']].append(product)
    #     res[product[3]].append(product)

    # # save product record
    # for cate in res:
    #     for item in res[cate]:
    #         product, scene, category, bbox = item['product'], item[
    #             'scene'], item['category'], item['bbox']
    #         product_id = create_product(
    #             conn, (product, scene, category, bbox[0], bbox[1], bbox[2], bbox[3]))
    #         item['id'] = product_id

    conn.commit()
    conn.close()

    i = 0
    # delete_image()
    # for cate in res:
    #     for product in res[cate]:
    #         # scene, bbox = product['scene'], product['bbox']
    #         scene = product[2]
    #         # download image
    #         # download_image(scene, product['id'])
    #         download_image(scene, product[0])
    #         i += 1
    #         print(i)

    # for cate in res:
    #     for product in res[cate]:
    #         # crop image according to bounding box
    #         crop_image(product[0], [product[4],
    #                                 product[5], product[6], product[7]])
    #         i += 1
    #         print(i)


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
    sql = ''' INSERT INTO products(product_id,scene,category,left,top,right,bottom)
              VALUES(?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, product)
    return cur.lastrowid


def select_product(conn):
    sql = "select * from products;"

    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    return rows


def update_product(conn, id, colors):
    sql = "update products set color1 = '"+str(colors[0])+"', color2 = '"+str(colors[1])+"', color3 = '" + \
        str(colors[2])+"', color4 = '"+str(colors[3]) + \
        "', color5 = '"+str(colors[4])+"' where id = '"+str(id)+"'"
    conn.execute(sql)


def reset_product(conn):
    # select product record by scene
    sql = "DELETE FROM products;"
    conn.execute(sql)

    sql = "update sqlite_sequence set seq = 0;"
    conn.execute(sql)


load_fashion_data()
