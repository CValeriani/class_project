import numpy as np
from shutil import rmtree
from PIL import Image
from io import BytesIO
from os import remove
from os import listdir as ls
from os import makedirs as mkdirs
from os.path import join, exists
from tensorflow.python_io import TFRecordWriter
from collections import namedtuple, OrderedDict
from object_detection.utils import dataset_util as datautil
import tensorflow as tsf
import pandas as pd
import os

class data_process():
    def split_csv(self, files, column):
        self.table = []
        self.data = namedtuple("data", ['filename', 'spec'])
        self.specs = files.groupby(column)
        
        for filename, pinpoint in zip(self.specs.groups.keys(), self.specs.groups):
            self.table.append(self.data(filename, self.specs.get_group(pinpoint)))
        return self.table

    def classification(self, model):
        if model == 'person': return 1
        else: return 0

    def create_record(self, column, path):
        self.jpgfile = tsf.gfile.GFile(join(path, "{}".format(column.filename)), "rb").read()
        self.jpgbytes = BytesIO(self.jpgfile)
        self.image = Image.open(self.jpgbytes)
        self.width, self.height = self.image.size

        self.filename = column.filename.encode('utf8')
        self.image_format = b'jpg'
        self.xmins = []
        self.xmaxs = []
        self.ymins = []
        self.ymaxs = []
        self.model = []
        self.classes = []

        for idx, row in column.spec.iterrows():
            self.xmins.append(row['xmin'] / self.width)
            self.xmaxs.append(row['xmax'] / self.width)
            self.ymins.append(row['ymin'] / self.height)
            self.ymaxs.append(row['ymax'] / self.height)
            self.model.append(row['class'].encode('utf8'))
            self.classes.append(data_process().classification(row['class']))

        self.mapping = tsf.train.Example(features=tsf.train.Features(\
            feature={\
            'image/height': datautil.int64_feature(self.height),\
            'image/width': datautil.int64_feature(self.width),\
            'image/filename': datautil.bytes_feature(self.filename),\
            'image/source_id': datautil.bytes_feature(self.filename),\
            'image/encoded': datautil.bytes_feature(self.jpgfile),\
            'image/format': datautil.bytes_feature(self.image_format),\
            'image/object/recbox/xmin': datautil.float_list_feature(self.xmins),\
            'image/object/recbox/xmax': datautil.float_list_feature(self.xmaxs),\
            'image/object/recbox/ymin': datautil.float_list_feature(self.ymins),\
            'image/object/recbox/ymax': datautil.float_list_feature(self.ymaxs),\
            'image/object/class/model': datautil.bytes_list_feature(self.model),\
            'image/object/class/label': datautil.int64_list_feature(self.classes),\
            }\
        ))
        return self.mapping

    def fetch_data(self, folder):
        # Initalization      
        self.map = []
        # -------------------------
        for files in ls(folder):
            for data in ls(join(folder, files)):
                if data.endswith(".csv"):
                    self.csv = pd.read_csv(join(folder, files, data))
                    self.spec = data_process().split_csv(files=self.csv, column="filename")
                    self.map.extend(self.spec)

            if not exists("records"): mkdirs("records")
            if files.startswith("train"):
                if not exists(join("records", "train")): mkdirs(join("records", "train"))
                if exists(join("records", "train", files+".record")): remove(join("records", "train", files+".record"))
                self.write = TFRecordWriter(join("records", "train", files+".record"))
            elif files.startswith("test"):  
                if not exists(join("records", "test")): mkdirs(join("records", "test"))          
                if exists(join("records", "test", files+".record")): remove(join("records", "test", files+".record"))
                self.write = TFRecordWriter(join("records", "test", files+".record"))
                
            for col in self.map:
                print("[>>] processing",col.filename, "record")
                self.record = data_process().create_record(col, join(folder, files))
                self.write.write(self.record.SerializeToString())            
            self.write.close()
        print("[OK] Done")

    def img_to_numpyarr(self, image):
        self.reshape = np.array(image.getdata()).astype(np.uint8)
        return self.reshape

    def image_open(self, files):
        self.src = Image.open(files)
        self.res = data_process().img_to_numpyarr(self.src)
        return self.res

    def junk_clean(self, path):
        rmtree(path)