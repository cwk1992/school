import pandas as pd
import numpy as np
from tqdm import tqdm
from database.database import Database


class ContentBasedFilter:
    def __init__(self):
        self.database = Database


abc = ContentBasedFilter()
print(abc)
