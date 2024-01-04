import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.exception import CustomException
from src.logger import logging
from src.components.data_transformation import DataTransformation, DataTransformationConfig
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_data_path:str=os.path.join("artifacts", "train.csv")
    test_data_path:str=os.path.join("artifacts", "test.csv")
    raw_data_path:str=os.path.join("artifacts", "raw_data.csv")

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config=DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the Data Ingestion Initialization")
        try:
            df=pd.read_csv("notebook/data/stud.csv")
            logging.info("Read the data set with shape {} as dataframe".format(df.shape))
            os.makedirs(os.path.dirname(self.data_ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.data_ingestion_config.raw_data_path, index=False, header=True)
            logging.info("train_test_split has initiated")
            train_set, test_set=train_test_split(df, test_size=0.2,random_state=20)
            train_set.to_csv(self.data_ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.test_data_path, index=False, header=True)
            logging.info("Ingestion of data Completed")
            logging.info("train_data_path:{}".format(self.data_ingestion_config.train_data_path))
            logging.info("test_data_path:{}".format(self.data_ingestion_config.test_data_path))
            logging.info("raw_data_path:{}".format(self.data_ingestion_config.raw_data_path))
            return(
                self.data_ingestion_config.train_data_path,
                self.data_ingestion_config.test_data_path
            )
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    obj=DataIngestion()
    train_data, test_data=obj.initiate_data_ingestion()
    
    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data, test_data)