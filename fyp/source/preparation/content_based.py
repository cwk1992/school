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

    color = {
        "Indian Red": "indian_red",
        "Light Coral": "light_coral",
        "Salmon": "salmon",
        "Dark Salmon": "dark_salmon",
        "Light Salmon": "light_salmon",
        "Crimson": "crimson",
        "Red": "red",
        "Firebrick ": "firebrick",
        "Dark Red": "dark_red",
        "Pink": "pink",
        "Light Pink": "light_pink",
        "Hot Pink": "hot_pink",
        "Deep Pink": "deep_pink",
        "Medium Violet Red": "medium_violet_red",
        "Pale Violet Red ": "pale_violet_red",
        "Coral": "coral",
        "Tomato": "tomato",
        "Orange Red": "orange_red",
        "Dark Orange": "dark_orange",
        "Orange": "orange",
        "Gold": "gold",
        "Yellow": "yellow",
        "Light Yellow": "light_yellow",
        "Lemon Chiffon": "lemon_chiffon",
        "Light Goldenrod Yellow": "light_goldenrod_yellow",
        "Papayawhip ": "papayawhip",
        "Moccasin ": "moccasin",
        "Peachpuff ": "peachpuff",
        "Pale Goldenrod": "pale_goldenrod",
        "Khaki ": "khaki",
        "Dark Khaki ": "dark_khaki",
        "Lavender": "lavender",
        "Thistle ": "thistle",
        "Plum ": "plum",
        "Violet": "violet",
        "Orchids": "orchids",
        "Fuchsia": "fuchsia",
        "Magenta": "magenta",
        "Medium Orchid": "medium_orchid",
        "Medium Purple": "medium_purple",
        "Rebeccapurple": "rebeccapurple",
        "Blue Violet": "blue_violet",
        "Dark Violet": "dark_violet",
        "Dark Orchid": "dark_orchid",
        "Dark Magenta": "dark_magenta",
        "Purple": "purple",
        "Indigo ": "indigo",
        "Slate Blue": "slate_blue",
        "Dark Slate Blue": "dark_slate_blue",
        "Medium Slate Blue": "medium_slate_blue",
        "Green Yellow": "green_yellow",
        "Chartreuse": "chartreuse",
        "Lawn Green": "lawn_green",
        "Lime": "lime",
        "Lime Green": "lime_green",
        "Pale Green": "pale_green",
        "Light Green": "light_green",
        "Medium Spring Green": "medium_spring_green",
        "Spring Green": "spring_green",
        "Medium Sea Green": "medium_sea_green",
        "Sea Green": "sea_green",
        "Forest Green": "forest_green",
        "Green": "green",
        "Dark Green": "dark_green",
        "Yellow Green": "yellow_green",
        "Olive Drab": "olive_drab",
        "Olive": "olive",
        "Darkolive Green": "darkolive_green",
        "Medium Aquamarine": "medium_aquamarine",
        "Dark Sea Green": "dark_sea_green",
        "Light Sea Green": "light_sea_green",
        "Dark Cyan": "dark_cyan",
        "Teal": "teal",
        "Aqua": "aqua",
        "Cyan": "cyan",
        "Light Cyan": "light_cyan",
        "Pale Turquoise": "pale_turquoise",
        "Aquamarine": "aquamarine",
        "Turquoise": "turquoise",
        "Medium Turquoise": "medium_turquoise",
        "Dark Turquoise": "dark_turquoise",
        "Cadet Blue": "cadet_blue",
        "Steel Blue": "steel_blue",
        "Lightsteel Blue": "lightsteel_blue",
        "Powder Blue": "powder_blue",
        "Light Blue": "light_blue",
        "Sky Blue": "sky_blue",
        "Lightsky Blue": "lightsky_blue",
        "Deepsky Blue": "deepsky_blue",
        "Dodger Blue": "dodger_blue",
        "Cornflower Blue": "cornflower_blue",
        "Mediumslate Blue": "mediumslate_blue",
        "Royal Blue": "royal_blue",
        "Blue": "blue",
        "Medium Blue": "medium_blue",
        "Dark Blue": "dark_blue",
        "Navy": "navy",
        "Midnight Blue": "midnight_blue",
        "Cornsilk": "cornsilk",
        "Blanched Almond": "blanched_almond",
        "Bisque": "bisque",
        "Navajo White": "navajo_white",
        "Wheat": "wheat",
        "Burly Wood": "burly_wood",
        "Tan": "tan",
        "Rosy Brown": "rosy_brown",
        "Sandy Brown": "sandy_brown",
        "Goldenrod": "goldenrod",
        "Dark Goldenrod": "dark_goldenrod",
        "Peru": "peru",
        "Chocolate": "chocolate",
        "Saddle Brown": "saddle_brown",
        "Sienna": "sienna",
        "Brown": "brown",
        "Maroon": "maroon",
        "White": "white",
        "Snow": "snow",
        "Honeydew": "honeydew",
        "Mint Cream": "mint_cream",
        "Azure": "azure",
        "Alice Blue": "alice_blue",
        "Ghost White": "ghost_white",
        "White Smoke": "white_smoke",
        "Seashell": "seashell",
        "Beige": "beige",
        "Old Lace": "old_lace",
        "Floral White": "floral_white",
        "Ivory": "ivory",
        "Antique White": "antique_white",
        "Linen": "linen",
        "Lavender Blush": "lavender_blush",
        "Misty Rose": "misty_rose",
        "Gainsboro": "gainsboro",
        "Light Gray": "light_gray",
        "Silver": "silver",
        "Dark Gray": "dark_gray",
        "Gray": "gray",
        "Dim Gray": "dim_gray",
        "Light Slate Gray": "light_slate_gray",
        "Slate Gray": "slate_gray",
        "Dark Slate Gray": "dark_slate_gray",
        "Black": "black"
    }

    for product in products:
        update_product(conn, product[0], color[product[8]])
        update_product(conn, product[0], color[product[9]])
        update_product(conn, product[0], color[product[10]])
        update_product(conn, product[0], color[product[11]])
        update_product(conn, product[0], color[product[12]])

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


def update_product(conn, id, color):
    sql = "update products set "+color+" = '1' where id = '"+str(id)+"'"
    conn.execute(sql)


def reset_product(conn):
    # select product record by scene
    sql = "DELETE FROM products;"
    conn.execute(sql)

    sql = "update sqlite_sequence set seq = 0;"
    conn.execute(sql)


load_fashion_data()
