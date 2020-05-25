import pandas as pd
import numpy as np
from tqdm import tqdm
from database.database import Database


class ContentBasedFilter:
    def __init__(self):
        self.database = Database()

    def get_products(self):
        return self.database.select_all('products')

    def get_user_products(self):
        return self.database.select_user_products()

    def tfidf(self):
        product_columns = ['id', 'product_id', 'scene', 'category', 'indian_red', 'light_coral', 'salmon', 'dark_salmon', 'light_salmon', 'crimson', 'red', 'firebrick', 'dark_red', 'pink', 'light_pink', 'hot_pink', 'deep_pink', 'medium_violet_red', 'pale_violet_red', 'coral', 'tomato', 'orange_red', 'dark_orange', 'orange', 'gold', 'yellow', 'light_yellow', 'lemon_chiffon', 'light_goldenrod_yellow', 'papayawhip', 'moccasin', 'peachpuff', 'pale_goldenrod', 'khaki', 'dark_khaki', 'lavender', 'thistle', 'plum', 'violet', 'orchids', 'fuchsia', 'magenta', 'medium_orchid', 'medium_purple', 'rebeccapurple', 'blue_violet', 'dark_violet', 'dark_orchid', 'dark_magenta', 'purple', 'indigo', 'slate_blue', 'dark_slate_blue', 'medium_slate_blue', 'green_yellow', 'chartreuse', 'lawn_green', 'lime', 'lime_green', 'pale_green', 'light_green', 'medium_spring_green', 'spring_green', 'medium_sea_green', 'sea_green', 'forest_green', 'green', 'dark_green', 'yellow_green', 'olive_drab', 'olive',
                           'darkolive_green', 'medium_aquamarine', 'dark_sea_green', 'light_sea_green', 'dark_cyan', 'teal', 'aqua', 'cyan', 'light_cyan', 'pale_turquoise', 'aquamarine', 'turquoise', 'medium_turquoise', 'dark_turquoise', 'cadet_blue', 'steel_blue', 'lightsteel_blue', 'powder_blue', 'light_blue', 'sky_blue', 'lightsky_blue', 'deepsky_blue', 'dodger_blue', 'cornflower_blue', 'mediumslate_blue', 'royal_blue', 'blue', 'medium_blue', 'dark_blue', 'navy', 'midnight_blue', 'cornsilk', 'blanched_almond', 'bisque', 'navajo_white', 'wheat', 'burly_wood', 'tan', 'rosy_brown', 'sandy_brown', 'goldenrod', 'dark_goldenrod', 'peru', 'chocolate', 'saddle_brown', 'sienna', 'brown', 'maroon', 'white', 'snow', 'honeydew', 'mint_cream', 'azure', 'alice_blue', 'ghost_white', 'white_smoke', 'seashell', 'beige', 'old_lace', 'floral_white', 'ivory', 'antique_white', 'linen', 'lavender_blush', 'misty_rose', 'gainsboro', 'light_gray', 'silver', 'dark_gray', 'gray', 'dim_gray', 'light_slate_gray', 'slate_gray', 'dark_slate_gray', 'black']
        user_column = ['id', 'name', 'password', 'email']

        # get product from database
        products = pd.read_sql_query(self.get_products(),
                                     self.database.conn)

        # get all categories
        df_item = products[['id', 'category']]

        # one-hot encoding for category
        category = pd.get_dummies(df_item['category'])

        # split columns for demo data
        category['T-shirt/top'] = category['T-shirt/top|Pullover|Shirt']
        category['Pullover'] = category['T-shirt/top|Pullover|Shirt']
        category['Shirt'] = category['T-shirt/top|Pullover|Shirt']
        category['Sandal'] = category['Sandal|Sneaker|Ankle boot']
        category['Sneaker'] = category['Sandal|Sneaker|Ankle boot']
        category['Ankle boot'] = category['Sandal|Sneaker|Ankle boot']

        # remove combined columns
        category = category.drop(
            columns=['T-shirt/top|Pullover|Shirt', 'Sandal|Sneaker|Ankle boot'])

        # normalized
        category_normalized = category.apply(
            lambda x: x/np.sqrt(category.sum(axis=1)))

        # create item profile
        df_item = pd.concat([df_item, category_normalized], axis=1)
        df_item.drop(columns='category', inplace=True)
        df_item.sort_values('id', inplace=True)
        df_item.set_index('id', inplace=True)

        # get user merge products
        df_user = pd.read_sql_query(self.get_user_products(),
                                    self.database.conn)

        df_final = df_user[df_user['user'].isin(df_item.index)]

        print(df_final.head())


abc = ContentBasedFilter()
abc.tfidf()
