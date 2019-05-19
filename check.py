import tensorflow as tsf

for example in tsf.python_io.tf_record_iterator("TsfRecord.tfrecord"):
    print(tsf.train.Example.FromString(example))