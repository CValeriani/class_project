from handler.data_handler import data_process as data
from tensorflow import keras
import tensorflow
from os.path import join

train = data(join("handler", "assets", "resources")).input_data()