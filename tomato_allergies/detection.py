#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 12:03:51 2019

@author: j-bd
"""
from tensorflow.keras.models import load_model
from vis.visualization import visualize_cam, overlay
from vis.utils import utils
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.cm as cm

class Detection:
    '''Class activation maps'''
    def __init__(self, model_path):
        '''Create a new object with the following base structure'''
        self.model = load_model(model_path)
        self.model.summary()

    def visualize_cam(self, img_path):
        '''Compute and display tomato activation maps for a picture'''
        img = utils.load_img(img_path, target_size=(300, 300))
        layer_idx = utils.find_layer_idx(self.model, 'dense_1')
        penultimate_layer = utils.find_layer_idx(self.model, 'max_pooling2d_2')
        cam = visualize_cam(
            self.model, layer_idx=layer_idx, filter_indices=1, seed_input=img,
            penultimate_layer_idx=penultimate_layer
        )
        jet_heatmap = np.uint8(cm.jet(cam)[..., :3] * 255)
        plt.figure("Class activation maps", figsize=(20.0, 5.0))
        plt.subplot(131)
        plt.title(img_path.split("/")[-1])
        plt.imshow(img)
        plt.subplot(132)
        plt.title("Activation maps")
        plt.imshow(cam)
        plt.subplot(133)
        plt.title("Overlay")
        plt.imshow(overlay(cam, img, alpha=0.25))
        plt.savefig(f"{img_path.split('/')[-1]}-class_activation_maps.png")
        return jet_heatmap, img

    def predict(self, img_path):
        '''Give an image prediction related to a model'''
        img_init = utils.load_img(img_path, target_size=(300, 300))
        img = np.array(img_init).astype('float32')/255
        img = np.expand_dims(img, axis=0)
        y_pred = self.model.predict(img)
        plt.figure(f"Prediction for {img_path.split('/')[-1]}")
        plt.title(f"Tomato prediction: {y_pred[0]}")
        plt.imshow(img_init)
        plt.savefig(f"{img_path.split('/')[-1]}-predict.png")

