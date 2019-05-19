import tensorflow as tsf        
from tensorflow import keras

class Models():
    def import_record(self, files):
        self.dataset = tsf.data.TFRecordDataset(files)
        self.dataset = Models().parse_data(self.dataset)
        self.rec_iter = self.dataset.make_one_shot_iterator()
        return self.rec_iter.get_next()

        # with tsf.Session() as start:
        #     start.run(self.iterator.initializer, feed_dict={self.buffer: files})


    def parse_data(self, dataset, batch_size=32):
        self.features = {\
            'image/height': tsf.FixedLenFeature([], tsf.int64),\
            'image/width': tsf.FixedLenFeature([], tsf.int64),\
            'image/source_id': tsf.FixedLenFeature([], tsf.string),\
            'image/encoded': tsf.FixedLenFeature([], tsf.string),\
            'image/format': tsf.FixedLenFeature([], tsf.string),\
            'image/object/recbox/xmin': tsf.VarLenFeature(tsf.float32),\
            'image/object/recbox/xmax': tsf.VarLenFeature(tsf.float32),\
            'image/object/recbox/ymin': tsf.VarLenFeature(tsf.float32),\
            'image/object/recbox/ymax': tsf.VarLenFeature(tsf.float32),\
            'image/object/class/model': tsf.VarLenFeature(tsf.string),\
            'image/object/class/label': tsf.VarLenFeature(tsf.int64),\
        }
        # --------------------------------
        def parse_func(example):
            print("[>>] Parsing example...")
            self.fileset = tsf.parse_example([example], self.features)
            print("[OK] Done")
            # Convert the result
            print("[>>] Converting result...")
            self.image = tsf.decode_raw(self.fileset['image/encoded'], tsf.uint8)
            self.image = tsf.cast(self.image, tsf.float32)
            self.height = tsf.cast(self.fileset['image/height'], tsf.int32)
            self.width = tsf.cast(self.fileset['image/width'], tsf.int32)
            self.source = self.fileset['image/source_id']
            self.format = self.fileset['image/format']
            self.xmin = self.fileset['image/object/recbox/xmin']
            self.xmax = self.fileset['image/object/recbox/xmax']
            self.ymin = self.fileset['image/object/recbox/ymin']
            self.ymax = self.fileset['image/object/recbox/ymax']
            self.model = self.fileset['image/object/class/model']
            self.label = tsf.cast(self.fileset['image/object/class/label'], tsf.int32)
            print("[OK] Done")

            return self.fileset
        # --------------------------------

        self.parse = dataset.apply(tsf.contrib.data.shuffle_and_repeat(2048, 1))
        self.parse = dataset.apply(tsf.contrib.data.map_and_batch(parse_func, 32))
        return self.parse

    # def create_model(self, features, label, mode, param):
    #     num_classes = 3
    #     self.net = features["image"]

    #     net = tsf.identity(net, name="input_tensor")
        
    #     net = tsf.reshape(net, [-1, 224, 224, 3])    

    #     net = tsf.identity(net, name="input_tensor_after")

    #     net = tsf.layers.conv2d(inputs=net, name='layer_conv1',
    #                         filters=32, kernel_size=3,
    #                         padding='same', activation=tsf.nn.relu)
    #     net = tsf.layers.max_pooling2d(inputs=net, pool_size=2, strides=2)

    #     net = tsf.layers.conv2d(inputs=net, name='layer_conv2',
    #                         filters=64, kernel_size=3,
    #                         padding='same', activation=tsf.nn.relu)
    #     net = tsf.layers.max_pooling2d(inputs=net, pool_size=2, strides=2)  

    #     net = tsf.layers.conv2d(inputs=net, name='layer_conv3',
    #                         filters=64, kernel_size=3,
    #                         padding='same', activation=tsf.nn.relu)
    #     net = tsf.layers.max_pooling2d(inputs=net, pool_size=2, strides=2)    

    #     net = tsf.contrib.layers.flatten(net)

    #     net = tsf.layers.dense(inputs=net, name='layer_fc1',
    #                         units=128, activation=tsf.nn.relu)  
        
    #     net = tsf.layers.dropout(net, rate=0.5, noise_shape=None, 
    #                         seed=None, training=(mode == tsf.estimator.ModeKeys.TRAIN))
        
    #     net = tsf.layers.dense(inputs=net, name='layer_fc_2',
    #                         units=num_classes)

    #     logits = net
    #     y_pred = tsf.nn.softmax(logits=logits)

    #     y_pred = tsf.identity(y_pred, name="output_pred")

    #     y_pred_cls = tsf.argmax(y_pred, axis=1)

    #     y_pred_cls = tsf.identity(y_pred_cls, name="output_cls")


    #     if mode == tsf.estimator.ModeKeys.PREDICT:
    #         spec = tsf.estimator.EstimatorSpec(mode=mode,
    #                                         predictions=y_pred_cls)
    #     else:
    #         cross_entropy = tsf.nn.sparse_softmax_cross_entropy_with_logits(labels=labels,
    #                                                                     logits=logits)
    #         loss = tsf.reduce_mean(cross_entropy)

    #         optimizer = tsf.train.AdamOptimizer(learning_rate=params["learning_rate"])
    #         train_op = optimizer.minimize(
    #             loss=loss, global_step=tsf.train.get_global_step())
    #         metrics = {
    #             "accuracy": tsf.metrics.accuracy(labels, y_pred_cls)
    #         }

    #         spec = tsf.estimator.EstimatorSpec(
    #             mode=mode,
    #             loss=loss,
    #             train_op=train_op,
    #             eval_metric_ops=metrics)
            
    #     return spec

    def create_graph(self, path):
        self.file = tsf.gfile.Open(path, "rb")
        self.graph = self.file.read()
        self.graph_def = tsf.GraphDef()
        self.graph_def.MergeFromString(self.graph)

        self.gr = tsf.get_default_graph()
        self.tensor_num
        # handle for input and output of tensors
        # self.opt = tsf.get_default_graph().get_operations()
        # self.tensorname = {}
        # self.tensordict = {}

        # for op in self.opt:
        #     for output in op.outputs:
        #         self.tensorname.update(output.name)

        