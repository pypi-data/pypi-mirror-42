import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import glob
import cv2
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
from tensorflow.core.framework import graph_pb2
import scipy.misc
import time
import copy
import base64
from io import BytesIO

import re

numbers = re.compile(r'(\d+)')


def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


# This is needed since the notebook is stored in the object_detection folder.
sys.path.append("..")
from object_detection.utils import ops as utils_ops

from utils import label_map_util

from utils import visualization_utils as vis_util

PATH_TO_CKPT = "C:/Users/TS-3/Desktop/gb_ai_sdk/frozen_inference_graph.pb"
PATH_TO_LABELS = "C:/Users/TS-3/Desktop/gb_ai_sdk/graph.pbtxt"
PATH_TO_TEST_IMAGES_DIR = "C:/Users/TS-3/Desktop/gb_ai_sdk/inp"
PATH_TO_OUTPUT_IMAGES_DIR = "C:/Users/TS-3/Desktop/gb_ai_sdk/outp"
VIDEO_NAME = "C:/Users/TS-3/Desktop/gb_ai_sdk/inp/test2.mp4"
detection_graph = None
category_index = None
sess = None
count =0
current_frame_car = []
previous_frame_car = []
current_frame_person= []
previous_frame_person = []
current_frame_bus = []
previous_frame_bus = []
current_frame_truck = []
previous_frame_truck = []
current_frame_motorcycle = []
previous_frame_motorcycle = []
current_frame_bicycle = []
previous_frame_bicycle = []

total_passed_vehicle = 0
count_car = 0
count_person = 0
count_truck = 0
count_motorcycle = 0
count_bus = 0
count_bicycle = 0
frame_count_frame = -1
previous_image = None

def path_to_model(str):
    global PATH_TO_CKPT
    PATH_TO_CKPT = str
    return PATH_TO_CKPT


def path_to_video(str):
    global VIDEO_NAME
    str.replace('\\','/')
    VIDEO_NAME = str
    return VIDEO_NAME


def path_to_label(str):
    global PATH_TO_LABELS
    PATH_TO_LABELS = str
    return PATH_TO_LABELS


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)


def path_to_image_directory(str):
    global PATH_TO_TEST_IMAGES_DIR
    PATH_TO_TEST_IMAGES_DIR = str
    return PATH_TO_TEST_IMAGES_DIR


def path_to_output_directory(str):
    global PATH_TO_OUTPUT_IMAGES_DIR
    PATH_TO_OUTPUT_IMAGES_DIR = str
    return PATH_TO_OUTPUT_IMAGES_DIR


# def run_inference_for_single_image(image, graph):
#     with graph.as_default():
#         with tf.Session() as sess:
#             # Get handles to input and output tensors
#             ops = tf.get_default_graph().get_operations()
#             all_tensor_names = {output.name for op in ops for output in op.outputs}
#             tensor_dict = {}
#             for key in [
#                 'num_detections', 'detection_boxes', 'detection_scores',
#                 'detection_classes', 'detection_masks'
#             ]:
#                 tensor_name = key + ':0'
#                 if tensor_name in all_tensor_names:
#                     tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
#                         tensor_name)
#             if 'detection_masks' in tensor_dict:
#                 # The following processing is only for single image
#                 detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
#                 detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
#                 # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
#                 real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
#                 detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
#                 detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
#                 detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
#                     detection_masks, detection_boxes, image.shape[0], image.shape[1])
#                 detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
#                 # Follow the convention by adding back the batch dimension
#                 tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)
#             image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
#             # Run inference
#             output_dict = sess.run(tensor_dict,feed_dict={image_tensor: np.expand_dims(image, 0)})
#             # all outputs are float32 numpy arrays, so convert types as appropriate
#             output_dict['num_detections'] = int(output_dict['num_detections'][0])
#             output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
#             output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
#             output_dict['detection_scores'] = output_dict['detection_scores'][0]
#             if 'detection_masks' in output_dict:
#                 output_dict['detection_masks'] = output_dict['detection_masks'][0]
#     return output_dict

def run_detection_on_video():
    NUM_CLASSES = 91
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    print(VIDEO_NAME)

    cap = cv2.VideoCapture(VIDEO_NAME)

    # Define the codec and create VideoWriter object
    width = cap.get(3)  # float
    height = cap.get(4)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(PATH_TO_OUTPUT_IMAGES_DIR + '/output.avi', fourcc, 20.0, (int(width), int(height)))
    count_frame=0
    while (cap.isOpened()):
        ret, frame = cap.read()
        #count_frame=0
        if ret == True:
            image_np = frame  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            # image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            count_frame+=1
            if count_frame%2==0:
                ts = time.clock()
                output_dict = run_object_detection(image_np)
                ts2 = time.clock()
                print(ts2 - ts)
            # Visualization of the results of a detection.
            # vis_util.visualize_boxes_and_labels_on_image_array(
            #     image_np,
            #     output_dict['detection_boxes'],
            #     output_dict['detection_classes'],
            #     output_dict['detection_scores'],
            #     category_index,
            #     instance_masks=output_dict.get('detection_masks'),
            #     use_normalized_coordinates=True,
            #     line_thickness=1)

            # write the flipped frame
                out.write(image_np)

                cv2.imshow('frame', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        else:
            break

    # Release everything if job is finished
    cap.release()
    out.release()
    cv2.destroyAllWindows()


# def run_detection_on_image():
#   NUM_CLASSES = 91
#   detection_graph = tf.Graph()
#   with detection_graph.as_default():
#       od_graph_def = tf.GraphDef()
#       with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
#           serialized_graph = fid.read()
#           od_graph_def.ParseFromString(serialized_graph)
#           tf.import_graph_def(od_graph_def, name='')

#   label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
#   categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
#   category_index = label_map_util.create_category_index(categories)

#   TEST_IMAGE_PATHS = glob.glob(PATH_TO_TEST_IMAGES_DIR+"/*.jpg")
#   TEST_IMAGE_PATHS=sorted(TEST_IMAGE_PATHS,key=numericalSort)

#   print(TEST_IMAGE_PATHS)

# # Size, in inches, of the output images.
#   IMAGE_SIZE = (12, 8)

#   for image_path in TEST_IMAGE_PATHS:
#       image = Image.open(image_path)
#       print(image_path.split('\\')[-1])
#       # the array based representation of the image will be used later in order to prepare the
#       # result image with boxes and labels on it.
#       image_np = load_image_into_numpy_array(image)
#       # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
#       image_np_expanded = np.expand_dims(image_np, axis=0)
#       # Actual detection.
#       ts = time.clock()
#       output_dict = run_inference_for_single_image(image_np, detection_graph)
#       ts2 = time.clock()
#       print(ts2-ts)
#       # Visualization of the results of a detection.
#       vis_util.visualize_boxes_and_labels_on_image_array(
#           image_np,
#           output_dict['detection_boxes'],
#           output_dict['detection_classes'],
#           output_dict['detection_scores'],
#           category_index,
#           instance_masks=output_dict.get('detection_masks'),
#           use_normalized_coordinates=True,
#           line_thickness=1)

#       scipy.misc.imsave(PATH_TO_OUTPUT_IMAGES_DIR+"/{}".format(image_path.split('\\')[-1]), image_np)

def _node_name(n):
    if n.startswith("^"):
        return n[1:]
    else:
        return n.split(":")[0]
def initialize():
    global detection_graph, category_index,sess
    input_graph = tf.Graph()
    with tf.Session(graph=input_graph):
        score = tf.placeholder(tf.float32, shape=(None, 1917, 90), name="Postprocessor/convert_scores")
        expand = tf.placeholder(tf.float32, shape=(None, 1917, 1, 4), name="Postprocessor/ExpandDims_1")
        for node in input_graph.as_graph_def().node:
            if node.name == "Postprocessor/convert_scores":
                score_def = node
            if node.name == "Postprocessor/ExpandDims_1":
                expand_def = node

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            dest_nodes = ['Postprocessor/convert_scores', 'Postprocessor/ExpandDims_1']

            edges = {}
            name_to_node_map = {}
            node_seq = {}
            seq = 0
            for node in od_graph_def.node:
                n = _node_name(node.name)
                name_to_node_map[n] = node
                edges[n] = [_node_name(x) for x in node.input]
                node_seq[n] = seq
                seq += 1

            for d in dest_nodes:
                assert d in name_to_node_map, "%s is not in graph" % d

            nodes_to_keep = set()
            next_to_visit = dest_nodes[:]
            while next_to_visit:
                n = next_to_visit[0]
                del next_to_visit[0]
                if n in nodes_to_keep:
                    continue
                nodes_to_keep.add(n)
                next_to_visit += edges[n]

            nodes_to_keep_list = sorted(list(nodes_to_keep), key=lambda n: node_seq[n])

            nodes_to_remove = set()
            for n in node_seq:
                if n in nodes_to_keep_list: continue
                nodes_to_remove.add(n)
            nodes_to_remove_list = sorted(list(nodes_to_remove), key=lambda n: node_seq[n])

            keep = graph_pb2.GraphDef()
            for n in nodes_to_keep_list:
                keep.node.extend([copy.deepcopy(name_to_node_map[n])])

            remove = graph_pb2.GraphDef()
            remove.node.extend([score_def])
            remove.node.extend([expand_def])
            for n in nodes_to_remove_list:
                remove.node.extend([copy.deepcopy(name_to_node_map[n])])

            with tf.device('/gpu:0'):
                tf.import_graph_def(keep, name='')
            with tf.device('/cpu:0'):
                tf.import_graph_def(remove, name='')

    NUM_CLASSES = 90
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES,
                                                                use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    sess = tf.Session(graph=detection_graph, config=tf.ConfigProto(allow_soft_placement=True))


def load_image_into_numpy_array(image):
    (im_width, im_height) = image.size
    return np.array(image.getdata()).reshape(
        (im_height, im_width, 3)).astype(np.uint8)


def run_vehicle_counting(img):
    import glob
    global count,count_car, count_person, count_truck, count_motorcycle, count_bus, count_bicycle, previous_frame_car,hold_count,hold_frame, current_frame_car
    global current_frame_person    
    global previous_frame_person
    global current_frame_bus
    global previous_frame_bus
    global current_frame_truck
    global previous_frame_truck
    global current_frame_motorcycle
    global previous_frame_motorcycle
    global current_frame_bicycle
    global previous_frame_bicycle
    global frame_count_frame,previous_image
    frame_count_frame +=1
    if frame_count_frame%2==0:
    #TEST_IMAGE_PATHS = glob.glob(PATH_TO_TEST_IMAGES_DIR+"/*.jpg")
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        score_out = detection_graph.get_tensor_by_name('Postprocessor/convert_scores:0')
        expand_out = detection_graph.get_tensor_by_name('Postprocessor/ExpandDims_1:0')
        score_in = detection_graph.get_tensor_by_name('Postprocessor/convert_scores_1:0')
        expand_in = detection_graph.get_tensor_by_name('Postprocessor/ExpandDims_1_1:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        #i = 0
        thresh_car = 15
        thresh_person = 3
        thresh_bus = 25
        thresh_truck = 25
        thresh_motorcycle = 5
        thresh_bicycle = 5
        #for _ in range(3):
        #print(TEST_IMAGE_PATHS[i])
        #image_path = TEST_IMAGE_PATHS[i]
        #i += 1
        #image = Image.open(img)
        #with open("imageToSave.png", "wb") as fh:
        #    fh.write(base64.decodebytes(img))
        #image = Image.open("imageToSave.png")
        image = Image.open(BytesIO(base64.b64decode(img)))
        img = np.array(image)
        print("img received")
        #image = Image.open("imageToSave.png")
        image_np = img
        ht, width, _ = img.shape
        roi = ht - 100
        #image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)

        start_time = time.time()
        (score, expand) = sess.run([score_out, expand_out], feed_dict={image_tensor: image_np_expanded})
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={score_in: score, expand_in: expand})
        #print ('Iteration %d: %.3f sec' % (i, time.time() - start_time))

        counter, csv_line, counting_mode, person, car, motorcycle, truck, bus, bicycle = vis_util.visualize_boxes_and_labels_on_image_array(current_frame_number = 1,
                                                                                                          image = image_np,
                                                                                                          mode = 1,
                                                                                                          color_recognition_status = 0,
                                                                                                          boxes = np.squeeze(boxes),
                                                                                                          classes = np.squeeze(classes).astype(np.int32),
                                                                                                          scores = np.squeeze(scores),
                                                                                                          category_index = category_index,
                                                                                                          y_reference = roi,
                                                                                                          deviation = 0,
                                                                                                          use_normalized_coordinates=True,
                                                                                                          line_thickness=1)
        cv2.line(image_np, (0, roi), (width, roi), (0, 0, 0xFF), 1)
        cv2.line(image_np, (0, int(roi+10)), (width, int(roi+10)), (0, 0xFF, 0), 1)
        #total_passed_vehicle = total_passed_vehicle + counter
        
        current_frame_car = car
        if len(previous_frame_car) != 0:
            car_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_car)):
                temp = 0
                for j in range(0,len(current_frame_car)):
                    if ((previous_frame_car[i] - thresh_car < current_frame_car[j]) and (previous_frame_car[i] + thresh_car > current_frame_car[j])):
                        car_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_car) - car_count >=0:
                count_car += len(current_frame_car) - car_count
            previous_frame_car = current_frame_car

        else:
            count_car +=len(current_frame_car)
            previous_frame_car=current_frame_car

        current_frame_person = person
        if len(previous_frame_person) != 0:
            person_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_person)):
                temp = 0
                for j in range(0,len(current_frame_person)):
                    if ((previous_frame_person[i] - thresh_person < current_frame_person[j]) and (previous_frame_person[i] + thresh_person > current_frame_person[j])):
                        person_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_person) - person_count >=0:
                count_person += len(current_frame_person) - person_count
            previous_frame_person = current_frame_person

        else:
            count_person +=len(current_frame_person)
            previous_frame_person=current_frame_person

        current_frame_bus = bus
        if len(previous_frame_bus) != 0:
            bus_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_bus)):
                temp = 0
                for j in range(0,len(current_frame_bus)):
                    if ((previous_frame_bus[i] - thresh_bus < current_frame_bus[j]) and (previous_frame_bus[i] + thresh_bus > current_frame_bus[j])):
                        bus_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_bus) - bus_count >=0:
                count_bus += len(current_frame_bus) - bus_count
            previous_frame_bus = current_frame_bus

        else:
            count_bus +=len(current_frame_bus)
            previous_frame_bus=current_frame_bus

        current_frame_truck = truck
        if len(previous_frame_truck) != 0:
            truck_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_truck)):
                temp = 0
                for j in range(0,len(current_frame_truck)):
                    if ((previous_frame_truck[i] - thresh_truck < current_frame_truck[j]) and (previous_frame_truck[i] + thresh_truck > current_frame_truck[j])):
                        truck_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_truck) - truck_count >=0:
                count_truck += len(current_frame_truck) - truck_count
            previous_frame_truck = current_frame_truck

        else:
            count_truck +=len(current_frame_truck)
            previous_frame_truck=current_frame_truck

        current_frame_motorcycle = motorcycle
        if len(previous_frame_motorcycle) != 0:
            motorcycle_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_motorcycle)):
                temp = 0
                for j in range(0,len(current_frame_motorcycle)):
                    if ((previous_frame_motorcycle[i] - thresh_motorcycle < current_frame_motorcycle[j]) and (previous_frame_motorcycle[i] + thresh_motorcycle > current_frame_motorcycle[j])):
                        motorcycle_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_motorcycle) - motorcycle_count >=0:
                count_motorcycle += len(current_frame_motorcycle) - motorcycle_count
            previous_frame_motorcycle = current_frame_motorcycle

        else:
            count_motorcycle +=len(current_frame_motorcycle)
            previous_frame_motorcycle=current_frame_motorcycle

        current_frame_bicycle = bicycle
        if len(previous_frame_bicycle) != 0:
            bicycle_count = 0
            # hold_size=len(hold_frame)
            # h = 0
            # while h<hold_size:
            #     print("inside hold")
            #     for c in range(0,len(current_frame)):
            #         if ((hold_frame[h] - thresh_car < current_frame[c]) and (hold_frame[h] + thresh_car > current_frame[c])):
            #             car_count +=1
            #     hold_count[h] -=1
            #     if hold_count[h] ==0:
            #         hold_count.remove(hold_count[h])
            #         hold_frame.remove(hold_frame[h])
            #         hold_size-=1
            #     h+=1
            for i in range(0,len(previous_frame_bicycle)):
                temp = 0
                for j in range(0,len(current_frame_bicycle)):
                    if ((previous_frame_bicycle[i] - thresh_bicycle < current_frame_bicycle[j]) and (previous_frame_bicycle[i] + thresh_bicycle > current_frame_bicycle[j])):
                        bicycle_count +=1
                        temp +=1
                # if temp==0:
                #     hold_frame.append(previous_frame[i])
                #     hold_count.append(2)

            if len(current_frame_bicycle) - bicycle_count >=0:
                count_bicycle += len(current_frame_bicycle) - bicycle_count
            previous_frame_bicycle = current_frame_bicycle

        else:
            count_bicycle +=len(current_frame_bicycle)
            previous_frame_bicycle=current_frame_bicycle
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(
        #     image_np,
        #     'person: ' + str(count_person) +
        #     ' motorcycle: '+str(count_motorcycle) + 
        #     ' car: '+str(count_car) +
        #     ' truck: ' +str(count_truck)+
        #     ' bicyle: '+str(count_bicycle)  +
        #     ' bus: '+str(count_bus),
        #     (10, 35),
        #     font,
        #     0.8,
        #     (0, 0, 0xFF),
        #     2,
        #     cv2.FONT_HERSHEY_SIMPLEX,
        #     )

        # try:
        #     #Counter for previous and current frame for car

        #     if tot_car[-1]-tot_car[-2] == 0:
        #         pass
        #     elif tot_car[-1]-tot_car[-2] >0:
        #         count_car += tot_car[-1]-tot_car[-2]
            #same for person
            # if tot_person[-1]-tot_person[-2] == 0:
            #     pass
            # elif tot_person[-1]-tot_person[-2] >0:
            #     count_person += tot_person[-1]-tot_person[-2]
            # #Same for truck
            # if tot_truck[-1]-tot_truck[-2] == 0:
            #     pass
            # elif tot_truck[-1]-tot_truck[-2] >0:
            #     count_truck += tot_truck[-1]-tot_truck[-2]
            # #Same for motorcycle
            # if tot_motorcycle[-1]-tot_motorcycle[-2] == 0:
            #     pass
            # elif tot_motorcycle[-1]-tot_motorcycle[-2] >0:
            #     count_motorcycle += tot_motorcycle[-1]-tot_motorcycle[-2]
            # #same for bicycle
            # if tot_bicycle[-1]-tot_bicycle[-2] == 0:
            #     pass
            # elif tot_bicycle[-1]-tot_bicycle[-2] >0:
            #     count_bicycle += tot_bicycle[-1]-tot_bicycle[-2]
            # #same for bus
            # if tot_bus[-1]-tot_bus[-2] == 0:
            #     pass
            # elif tot_bus[-1]-tot_bus[-2] >0:
            #     count_bus += tot_bus[-1]-tot_bus[-2]

            # font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(
            #     image_np,
            #     'person: ' + str(count_person) +
            #     ' truck: '+str(count_truck) + 
            #     ' car: '+str(count_car)  + 
            #     ' current_count: ' +str(tot_car[-1])+
            #     ' previous_count: '+str(tot_car[-2])  +
            #     ' bus: '+str(count_bus),
            #     (10, 35),
            #     font,
            #     0.8,
            #     (0, 0, 0xFF),
            #     2,
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     )
        # except:
        #     print('exception')
        #     count_car +=tot_car[-1]
        #     count_motorcycle += tot_motorcycle[-1]
        #     count_bus += tot_bus[-1]
        #     count_person += tot_person[-1]
        #     count_bicycle += tot_bicycle[-1]
        #     count_truck += tot_truck[-1]
            # 
        # insert information text to video frame
                       
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(
            image_np,
            'ROI Line',
            (545, roi-10),
            font,
            0.6,
            (0, 0, 0xFF),
            1,
            cv2.LINE_AA,
            )
        scipy.misc.imsave(PATH_TO_OUTPUT_IMAGES_DIR + "/Frame_{}.jpg".format(count), image_np)
        im = Image.fromarray(image_np)
        with open(PATH_TO_OUTPUT_IMAGES_DIR + "/Frame_{}.jpg".format(count), "rb") as image_file:
            b64string = base64.b64encode(image_file.read())
        
        #print(b64string)
        count+=1
        arr = []
        arr.append(b64string)
        arr.append(count_person)
        arr.append(count_car)
        arr.append(count_bus)
        arr.append(count_truck)
        previous_image = arr
        return arr
    else:
        return previous_image

def run_object_detection(img):
    import glob
    global count,frame_count_frame,previous_image
    frame_count_frame +=1
    if frame_count_frame%2==0:
    #TEST_IMAGE_PATHS = glob.glob(PATH_TO_TEST_IMAGES_DIR+"/*.jpg")
        image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
        score_out = detection_graph.get_tensor_by_name('Postprocessor/convert_scores:0')
        expand_out = detection_graph.get_tensor_by_name('Postprocessor/ExpandDims_1:0')
        score_in = detection_graph.get_tensor_by_name('Postprocessor/convert_scores_1:0')
        expand_in = detection_graph.get_tensor_by_name('Postprocessor/ExpandDims_1_1:0')
        detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
        detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
        detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
        num_detections = detection_graph.get_tensor_by_name('num_detections:0')
        i = 0
        #for _ in range(3):
        #print(TEST_IMAGE_PATHS[i])
        #image_path = TEST_IMAGE_PATHS[i]
        #i += 1
        #image = Image.open(img)
        #with open("imageToSave.png", "wb") as fh:
        #    fh.write(base64.decodebytes(img))
        #image = Image.open("imageToSave.png")
        image = Image.open(BytesIO(base64.b64decode(img)))
        img = np.array(image)
        print("img received")
        #image = Image.open("imageToSave.png")
        image_np = img
        #image_np = load_image_into_numpy_array(image)
        image_np_expanded = np.expand_dims(image_np, axis=0)

        start_time = time.time()
        (score, expand) = sess.run([score_out, expand_out], feed_dict={image_tensor: image_np_expanded})
        (boxes, scores, classes, num) = sess.run(
            [detection_boxes, detection_scores, detection_classes, num_detections],
            feed_dict={score_in: score, expand_in: expand})
        #print ('Iteration %d: %.3f sec' % (i, time.time() - start_time))
        font = cv2.FONT_HERSHEY_SIMPLEX
        # cv2.putText(
        #     image_np,
        #     str(frame_count_frame),
        #     (545, 300-10),
        #     font,
        #     10,
        #     (0, 0, 0xFF),
        #     2,
        #     cv2.LINE_AA,
        #     )
        vis_util.visualize_boxes_and_labels_on_image_array2(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4)

        scipy.misc.imsave(PATH_TO_OUTPUT_IMAGES_DIR + "/Frame_{}.jpg".format(count), image_np)
        im = Image.fromarray(image_np)
        with open(PATH_TO_OUTPUT_IMAGES_DIR + "/Frame_{}.jpg".format(count), "rb") as image_file:
            b64string = base64.b64encode(image_file.read())

        #print(b64string)
        count+=1
        previous_image = b64string
        return b64string
    else:
        return previous_image
    