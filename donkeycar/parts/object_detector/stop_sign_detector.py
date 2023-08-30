import numpy as np
import cv2
import time
import random
import collections
"""
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
"""
from pycoral.utils.dataset import read_label_file
from pycoral.adapters import common
from pycoral.utils.edgetpu import make_interpreter

from PIL import Image
from matplotlib import cm
import os
import urllib.request


class StopSignDetector(object):
    '''
    Requires an EdgeTPU for this part to work

    This part will run a EdgeTPU optimized model to run object detection to detect a stop sign.
    We are just using a pre-trained model (MobileNet V2 SSD) provided by Google.
    '''

    def download_file(self, url, filename):
        if not os.path.isfile(filename):
            urllib.request.urlretrieve(url, filename)

    def __init__(self, min_score, show_bounding_box, max_reverse_count=0, reverse_throttle=-0.5, debug=False):
        MODEL_FILE_NAME = "ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
        LABEL_FILE_NAME = "coco_labels.txt"

        MODEL_URL = "https://github.com/google-coral/edgetpu/raw/master/test_data/ssd_mobilenet_v2_coco_quant_postprocess_edgetpu.tflite"
        LABEL_URL = "https://dl.google.com/coral/canned_models/coco_labels.txt"

        self.download_file(MODEL_URL, MODEL_FILE_NAME)
        self.download_file(LABEL_URL, LABEL_FILE_NAME)

        self.last_5_scores = collections.deque(np.zeros(5), maxlen=5)
        self.interpreter = make_interpreter(MODEL_FILE_NAME)
        self.interpreter.allocate_tensors()
        self.labels = read_label_file(LABEL_FILE_NAME)

        self.STOP_SIGN_CLASS_ID = 12
        self.min_score = min_score
        self.show_bounding_box = show_bounding_box
        self.debug = debug

        # reverse throttle related
        self.max_reverse_count = max_reverse_count
        self.reverse_count = max_reverse_count
        self.reverse_throttle = reverse_throttle
        self.is_reversing = False

    def convertImageArrayToPILImage(self, img_arr):
        img = Image.fromarray(img_arr.astype('uint8'), 'RGB')

        return img

    '''
    Return an object if there is a traffic light in the frame
    '''
    def detect_stop_sign (self, img_arr):
        img = self.convertImageArrayToPILImage(img_arr)
        resized_img = img.resize(common.input_size(self.interpreter), Image.Resampling.LANCZOS)
        common.set_input(self.interpreter, resized_img)
        self.interpreter.invoke()
        ans = [dict(zip(
            ['detection_boxes', 'detection_classes', 'detection_scores'], obj))
              for obj in zip(
                  common.output_tensor(self.interpreter, 0).copy()[0],
                  common.output_tensor(self.interpreter, 1).copy()[0],
                  common.output_tensor(self.interpreter, 2).copy()[0]
              )]
        max_score = 0
        traffic_light_obj = None
        if ans:
            for obj in ans:
                if (obj['detection_classes'] == self.STOP_SIGN_CLASS_ID):
                    if self.debug:
                        print("stop sign detected, score = {}".format(obj.score))
                    if (obj['detection_scores'] > max_score):
                        print(obj['detection_boxes'])
                        traffic_light_obj = obj
                        max_score = obj['detection_scores']

        # if traffic_light_obj:
        #     self.last_5_scores.append(traffic_light_obj.score)
        #     sum_of_last_5_score = sum(list(self.last_5_scores))
        #     # print("sum of last 5 score = ", sum_of_last_5_score)

        #     if sum_of_last_5_score > self.LAST_5_SCORE_THRESHOLD:
        #         return traffic_light_obj
        #     else:
        #         print("Not reaching last 5 score threshold")
        #         return None
        # else:
        #     self.last_5_scores.append(0)
        #     return None

        return traffic_light_obj

    def draw_bounding_box(self, traffic_light_obj, img_arr):
        """xmargin = (traffic_light_obj.bounding_box[1][0] - traffic_light_obj.bounding_box[0][0]) *0.1

        traffic_light_obj.bounding_box[0][0] = traffic_light_obj.bounding_box[0][0] + xmargin
        traffic_light_obj.bounding_box[1][0] = traffic_light_obj.bounding_box[1][0] - xmargin

        ymargin = (traffic_light_obj.bounding_box[1][1] - traffic_light_obj.bounding_box[0][1]) *0.05

        traffic_light_obj.bounding_box[0][1] = traffic_light_obj.bounding_box[0][1] + ymargin
        traffic_light_obj.bounding_box[1][1] = traffic_light_obj.bounding_box[1][1] - ymargin"""
        box = traffic_light_obj['detection_boxes']
        height, width = img_arr.shape[:2]
        pt1 = ( (box[1]*width).astype(int),
                (box[0]*height).astype(int))
        pt2 = ( (box[3]*width).astype(int), 
                (box[2]*height).astype(int))
        cv2.rectangle(img_arr, pt1, pt2, (0, 255, 0), 2)
        """cv2.rectangle(img_arr, tuple(traffic_light_obj.bounding_box[0].astype(int)),
                        tuple(traffic_light_obj.bounding_box[1].astype(int)), (0, 255, 0), 2)"""
        print(pt1)
        print(pt2)

    def run(self, img_arr, throttle, debug=False):
        if img_arr is None:
            return throttle, img_arr

        # Detect traffic light object
        traffic_light_obj = self.detect_stop_sign(img_arr)

        if traffic_light_obj or self.is_reversing:
            if self.show_bounding_box and traffic_light_obj != None:
                self.draw_bounding_box(traffic_light_obj, img_arr)
            
            # Set the throttle to reverse within the max reverse count when detected the traffic light object
            if self.reverse_count < self.max_reverse_count:
                self.is_reversing = True
                self.reverse_count += 1
                return self.reverse_throttle, img_arr
            else:
                self.is_reversing = False
                return 0, img_arr
        else:
            self.is_reversing = False
            self.reverse_count = 0
            return throttle, img_arr
