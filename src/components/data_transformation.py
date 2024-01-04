import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
import pandas as pd 
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from dataclasses import dataclass

@dataclass
class DataTransformationConfig:
    preprocessor_obj_path=os.path.join("artifacts", "preprocessor.pkl")

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()  

    def get_data_transformer_object(self):
        """
        This function is responsible for data transformation 
        """
        try:
            numerical_columns=['reading_score','writing_score']
            categorical_columns=[
                'gender',
                'race_ethnicity',
                'parental_level_of_education',
                'lunch',
                'test_preparation_course'
            ]
            num_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="median")),
                    ("scalar", StandardScaler(with_mean=False)) 
                ]
            )
            categorical_pipeline=Pipeline(
                steps=[
                    ("imputer",SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder()),
                    ("scalar", StandardScaler(with_mean=False)) 
                ]
            )
            logging.info("Catergorical Pipeline Created")
            logging.info("Numerical Pipeline Created")
            logging.info("Catergorical Columns {}".format(categorical_columns))
            logging.info("Numerical Columns {}".format(numerical_columns))
            preprocessor=ColumnTransformer(
                [("num_pipeline", num_pipeline, numerical_columns),
                ("cat_pipeline", categorical_pipeline, categorical_columns)]
            )
            return preprocessor
        except Exception as e:
            raise CustomException(e, sys)    
        
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)
            logging.info("Read the train data set with shape {} as dataframe".format(train_df.shape))
            logging.info("Read the test data set with shape {} as dataframe".format(test_df.shape))
            preprocessor_object=self.get_data_transformer_object()
            target_column_name='math_score'
            numerical_columns=['reading_score','writing_score']

            input_feature_train_df=train_df.drop(columns=[target_column_name], axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name], axis=1)
            target_feature_test_df=test_df[target_column_name]

            input_feature_train_arr=preprocessor_object.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessor_object.transform(input_feature_test_df)

            train_arr=np.c_[
                input_feature_train_arr, np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                input_feature_test_arr, np.array(target_feature_test_df)
            ]
            logging.info("Saving preprocessor object")
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_path,
                obj=preprocessor_object
            )
            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_path
            )
        except Exception as e:
            raise CustomException(e, sys)        