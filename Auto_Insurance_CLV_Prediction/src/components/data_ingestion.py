import os
import sys


import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass



@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('data','processed','train.csv')
    test_data_path: str = os.path.join('data','processed','test.csv')
    raw_data_path: str = os.path.join('data','processed','data.csv')


class DataIngestion:
    def __init__(self):
        pass