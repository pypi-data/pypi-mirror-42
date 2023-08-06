#encoding=UTF-8
import numpy as np
import os
import cv2
import sys
os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
import tensorflow as tf
import datatime
from PIL import Image
from distutils.sysconfig import get_python_lib
import pdb

from utils import label_map_util

class hand_detector:
    def __init__(self, modelversion=0):
        self.site_package_path = get_python_lib()
        if modelversion == 0:
           path_to_ckpt = os.path.join(self.site_package_path, 'hd_llz/models/v2_our6_rfcnmv_anchor12_320_500000')
        if modelversion == 1:
           path_to_ckpt = os.path.join(self.site_package_path, 'hd_llz/models/v2_our6_rfcnmv_anchor9_180_369818')
        path_to_labels = os.path.join(self.site_package_path, 'hd_llz/data/hand_label_map.pbtxt')
        num_classes = 1
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(path_to_ckpt, 'rb') as fid:
                self.serialized_graph = fid.read()
                od_graph_def.ParseFromString(self.serialized_graph)
                tf.import_graph_def(od_graph_def, name='')
        self.label_map = label_map_util.load_labelmap(path_to_labels)
        self.categories = label_map_util.convert_label_map_to_categories(self.label_map, max_num_classes=num_classes, use_display_name=True)
        self.category_index = label_map_util.create_category_index(self.categories)

        self.sess = None
        with self.detection_graph.as_default():
           self.sess = tf.Session(graph=self.detection_graph)


    def load_image_into_numpy_array(self,image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

    def get_predict_boxes_and_scores_use_nms(image, boxes, classes, scores, category_index, thresh = 0.3, confidence_thresh=0.5):
        #pdb.set_trace()
        im_width, im_height = image.size
        wid_hei= np.array([[im_height], [im_width], [im_height], [im_width]])
        wid_hei_array = np.stack(wid_hei,axis=1)
        bboxes = wid_hei_array * boxes

        dets = np.hstack((bboxes, scores[:, np.newaxis])).astype(np.float32)
        x1 = dets[:, 1]
        y1 = dets[:, 0]
        x2 = dets[:, 3]
        y2 = dets[:, 2]
        scores1 = dets[:,4]
        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores1.argsort()[::-1]     

        keep = []
        while order.size > 0:
            i = order[0]
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])
            w = np.maximum(0.0, xx2 - xx1 + 1)
            h = np.maximum(0.0, yy2 - yy1 + 1)
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)
            inds = np.where(ovr <= thresh)[0]
            order = order[inds + 1]

        dets_nms = dets[keep,:]
        print (dets_nms.shape)

        inds_dets_nms_confidence = np.where(dets_nms[:, -1] >= confidence_thresh)[0]
        if len(inds_dets_nms_confidence) == 0:
           dets_nms_confidence = []
        else:
           dets_nms_confidence = dets_nms[inds_dets_nms_confidence,:]
        print (dets_nms_confidence.shape)
        
        hand_num = 0
        hand_num = dets_nms_confidence.shape[0]
        xmin = dets_nms_confidence[:, 1]
        ymin = dets_nms_confidence[:. 0]
        xmax = dets_nms_confidence[:, 3]
        ymax = dets_nms_confidence[:, 2]
        center_x = (xmin + xmax) * 0.5
        center_y = (ymin + ymax) * 0.5
        rect = dets_nms_confidence[:, [1,0,3,2,4]]
        #return keep, inds_dets_nms_confidence, dets_nms, dets_nms_confidence
        return hand_num, center_x, center_y, rect


    def detect_hand_predict(self,image)：
        image_np = self.load_image_into_numpy_array(image)       
        image_np_expanded = np.expand_dims(image_np, axis=0)      
        image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')
        boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')
        scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
        classes = self.detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

        start = datetime.datetime.now()               #llz
        (boxes, scores, classes, num_detections) = self.sess.run(
              [boxes, scores, classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
        end = datetime.datetime.now()                 #llz
        single_time = (end - start).total_seconds()
                  
        hand_num, center_x, center_y, rect = self.get_predict_boxes_and_scores_use_nms(image, np.squeeze(boxes), np.squeeze(classes).astype(np.int32), np.squeeze(scores), self.category_index, thresh = 0.3, confidence_thresh=0.5)
        return (hand_num, center_x, center_y, rect, single_time)

    def test(self):
        hd3 = hand_detector()
        imf = os.path.join(self.site_package_path, 'hd_llz/data/test.png')
        #print (imf
        image = cv2.imread(imf)
        print(hd3.detect_hand_predict(image))

def draw_rect(img, savepath, left, top, right, bottom):
    cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 3)
    cv2.imwrite(savepath, img)
    return img




if __name__=="__main__":
    dirname='/data1/mingmingzhao/data_sets/no_hand_data/'
    #hd3=HandDetector3(int(sys.argv[1]))
    hd3=hand_detector()
    hd3.test()
    ci=0 # the count of image
    ch=0 # the count of hand
    ts=0 # avg of time cost
    for f in os.listdir(dirname):
       if f.endswith('.jpg'):
        imf=os.path.join(dirname,f)
        print(imf)
        image=cv2.imread(imf)
        hand_num, center_x, center_y, rect, tc = hd3.detect_hand_predict(image)
        if hand_num>0:
            ch+=1
        if ci>1:
           ts+=tc
           print("%d/%d,%fs,%fs,%fHz avg"%(ch,ci,tc,ts/(ci-1),(ci-1)/ts))
        ci+=1





