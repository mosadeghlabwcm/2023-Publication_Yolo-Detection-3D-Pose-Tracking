import os, shutil
import glob
import pickle
from tqdm import tqdm

from keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold
import time

# Imported for image viewing
import matplotlib.pyplot as plt
from PIL import Image
from IPython.display import display
import cv2
from skimage.io import imread

import pandas as pd
import numpy as np
import math
from math import sqrt
import random

from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from statistics import mean, median, mode, stdev
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

import tensorflow as tf
from tensorflow.keras.models import *
from tensorflow.keras.preprocessing.image import img_to_array, load_img
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras import layers
from tensorflow.keras.layers import Dense, Conv1D, Flatten, MaxPooling1D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

def get_img_group_name(imgID, method):
    """
    Get the group name of the images and their augmentations
    
    Parameters:
    imgID: the id of the image
    method: different methods based on different format
    
    Return:
    image group name
    """
    if method == 1:
        elements = imgID.split('_')
        if len(elements)>2:
            return imgID
        else:
            return elements[0]
    elif method == 2:
        elements = imgID.split('-')
        if len(elements) >= 2:
            return elements[-2] + '-' + elements[-1]
        else:
            return imgID
        
def revert_image_normalization(images, image_mean):
    images = np.round(images + image_mean).astype(int)
    return images

def label_anchor_box(x, y, anc_x_y):
    """Label anchor boxes, 0 means no catheter tip in the anchor box, 1 means with catheter tip in the anchor box
    input:
    x: x label of the catheter tip
    y: y label of the catheter tip
    anc_x_y: coordinates of anchor boxes
    
    return:
    anc_box_labels: List 
    """
    anc_box_labels = []
    for idx, x_y in enumerate(anc_x_y):
        x1_anc = x_y[0]
        x2_anc = x_y[1]
        y1_anc = x_y[2]
        y2_anc = x_y[3]

        if x1_anc<= x <= x2_anc and y1_anc<= y <= y2_anc:
            anc_box_labels.append(1)
        else:
            anc_box_labels.append(0)
    return anc_box_labels

def calculate_local_coords(x, y, anc_box_index, anc_x_y):
    """Calculate the co-ordinates of the catheter tip in the zoomed in region
    """
    x1_anc, x2_anc, y1_anc, y2_anc = anc_x_y[anc_box_index]
    x_local = x - x1_anc
    y_local = y - y1_anc
    
    return [x_local, y_local]

def custom_loss(y_actual, y_pred):
    """ The euclidean distance loss with a soft loss implementation
    """
    x1 = y_actual[:, 0]
    y1 = y_actual[:, 1]
    
    x2 = y_pred[:, 0]
    y2 = y_pred[:, 1]
    
    threshold = (6 / 512)**2
    distance = (x2 - x1)**2 + (y2 - y1)**2 
    distance_alter = tf.zeros_like(distance)
    distance_final = tf.where(distance > threshold, distance, distance_alter)
    
    return tf.reduce_mean(distance_final)

def custom_soft_loss(y_actual, y_pred):
    """ The euclidean distance loss with a soft loss implementation
    """
    x1 = y_actual[:, 0]
    y1 = y_actual[:, 1]
    
    x2 = y_pred[:, 0]
    y2 = y_pred[:, 1]
    
    threshold = (6 / 512)**2
    distance = (x2 - x1)**2 + (y2 - y1)**2 
    distance_alter = tf.zeros_like(distance)
    distance_final = tf.where(distance > threshold, distance, distance_alter)
    
    return tf.reduce_mean(distance_final)

def scaler_inverse_transform(normalized_y, scaler):
    return scaler.inverse_transform(normalized_y)

def calculateDistance(x1,y1,x2,y2):
    """ calculate euclidean distance between points from CAD design and retrieved affined points from images"""
    dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def SinglecalculateDistance(x1,x2):
    """ calculate euclidean distance between points from CAD design and retrieved affined points from images"""
    dist = np.sqrt((x2 - x1)**2)
    return dist