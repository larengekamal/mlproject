import os
import sys
import pandas as pd 
import numpy as np 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.exception import CustomException
from src.logger import logging

def save_object(file_path, obj):
    try:
        pass
    except Exception as e:
            raise CustomException(e, sys)  