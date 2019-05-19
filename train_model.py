from handler.model_handler import Models
import numpy as np
import tensorflow as tsf
from os.path import join

import subprocess as sp
sp.call("cls", shell=True)
tsf.enable_eager_execution()

# Get records from TFRecord
dataset = Models().import_record(join("records", "TsfRecord.tfrecord"))
print(dataset)

# Train the model
# feature_column = [tsf.feature_column.numeric_column(key='image/encoded',shape=(784,))]
# model = tsf.estimator.Estimator(model=Models().create_model, model_dir="datasets/")
# model.train(lambda:dataset(32), steps=200)

# print("success")
# # define type of features columns to be used on model.
# column = [tsf.feature_column.numeric_column(key='image',shape=(784,))]

# # define  model
# model = tsf.estimator.DNNClassifier([300,400],n_classes=1,feature_columns=column)

# # Train Models
# print("[>>] Training Dataset...")
# model.train(lambda:Import_Tfrecord(32), steps=1)
    
