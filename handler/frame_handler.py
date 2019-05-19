import cv2
import imutils
import threading as thr
import sys
from os.path import join
import numpy as np
import tensorflow as tsf
from object_detection.utils import label_map_util as labelmap
from object_detection.utils import visualization_utils as visual

# Configuration:
class_num = 1
model_name = "infer_graph"
ckpt_path = join("")
label_path = join("data", "item_map.pbtxt")

class Model():
    def __init__(self):
        self.label_map = labelmap.load_labelmap(label_path)
        self.categories = labelmap.convert_label_map_to_categories(self.label_map, max_num_classes=class, use_display_name=True)
        self.category_index = labelmap.create_category_index(self.categories)

class Graph():
    def load_Tfmodel(self):
        self.map = Model()
        self.detect_graph = tsf.Graph().as_default()
        self.graph_def = tsf.GraphDef()
        self.file = tsf.gfile.GFile(ckpt_path, 'rb')
        self.serialized = self.file.read()

        self.graph_def.ParseFromString(self.serialized)
        tsf.import_graph_def(self.graph_def, name = "")

        return tsf.Session(graph=self.detect_graph), self.detect_graph

    def processing(self, sess, graph, frame)
        # Input tensor
        self.image_tensor = graph.get_tensor_by_name('image_tensor:0')
        # Output tensor
        self.detect_box = graph.get_tensor_by_name('detection_boxes:0')
        self.detect_score = graph.get_tensor_by_name('detection_scores:0')
        self.detect_class = graph.get_tensor_by_name('detection_classes:0')
        self.detect_num = graph.get_tensor_by_name('num_detections:0')

        sess.run(['detection_boxes', 'detection_scores', 'detection_classes', 'num_detections'],\
                    feed_dict={'image_tensor': self.frame_expand}\
                )
        return self.detect_box, self.detect_score, self.detect_class, self.detect_num
        
class Framework():
    def __init__(self, media):
        self.vidstream = cv2.VideoCapture(media)
        self.wsize = self.vidstream.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.hsize = self.vidstream.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        (self.output, self.frame) = self.vidstream.read()
        return self.output, self.frame

    def analyze_feed(self):
        while True:
            self.conn, self.frames = self.get_frame()
            if self.conn == True:
                # Process the Image here
                self.frame_expand = np.expand_dims(self.frame_sample, axis=0)
                self.sess self.graph = Graph().load_Tfmodel()
                (self.box, self.score, self.type, self.num) = Graph().processing(self.sess, self.graph, self.frames)
                # Draw square around person recognized by system
                visual.visualize_boxes_and_labels_on_image_array(\
                    self.frames,\
                    np.squeeze(self.box),\
                    np.squeeze(self.type).astype(np.int32),\
                    np.squeeze(self.score),\
                    category_index,\
                    use_normalized_coordinates=True,\
                    line_thickness=4,\
                    min_score_thresh=0.65)\
                )
                # Display the frame ~ for display, we only need to resize it
                self.frame_output = Frame_control(self.frames).frame_outlook()
                cv2.imshow("Video Stream", self.frame_output)
                cv2.waitKey(33)
                if cv2.waitKey(66) & 0xFF == ord('\x1b'): break
            else: break 
        return False      

    def __del__(self):
        if self.vidstream.isOpened: self.vidstream.release()

class Frame_control():
    def __init__(self, frame):
        self.frame = frame

    def frame_outlook(self):
        # Resize the frame
        self.frame_resized = imutils.resize(self.frame, width=600, height=400)
        return self.frame_resized

    def rework_frame(self):
        # Resize the frame
        self.frame_resized = imutils.resize(self.frame, width=600, height=400)
        # Convert frame into Grayscale
        self.frame_fixed = cv2.cvtColor(self.frame_resized, cv2.COLOR_BGR2GRAY)
        return self.frame_fixed