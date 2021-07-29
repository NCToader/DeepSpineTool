# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 08:28:39 2019

@author: Marcos
https://bretahajek.com/2017/04/importing-multiple-tensorflow-models-graphs/
https://stackoverflow.com/questions/41990014/load-multiple-models-in-tensorflow/51290092
https://engineering.taboola.com/more-than-one-graph-code-reuse-in-tensorflow/
https://stackoverflow.com/questions/35955144/working-with-multiple-graphs-in-tensorflow

https://www.easy-tensorflow.com/tf-tutorials/basics/save-and-restore
https://stackoverflow.com/questions/33759623/tensorflow-how-to-save-restore-a-model
https://cv-tricks.com/tensorflow-tutorial/save-restore-tensorflow-models-quick-complete-tutorial/
https://stackabuse.com/tensorflow-save-and-restore-models/
"""

import os
from pathlib import Path
import csv
import math
from pathlib import Path

# import cv2
from skimage import io, util
import tensorflow as tf

print(tf.__version__)
from tensorflow.python.keras import Model
from tqdm import tqdm

import os

import math
from pathlib import Path
from shutil import copyfile

from tensorflow.keras import mixed_precision

from app.plugins.utils.segmentation.parser import YAMLConfig
from app.plugins.utils.image.segmentation.confocalNeuro.UNet import UNet3D, UNet3DDeep, VNet
import tensorflow as tf
import numpy as np
import random
import argparse

models_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / 'models'

try:
    import tensorflow.compat.v1 as tf

    tfVer = 2
except:
    import tensorflow as tf

    tfVer = 1

from tensorflow.python.client import device_lib as tfDevLib

from app.core.utils import SingletonDecorator


# https://www.tensorflow.org/guide/gpu
def init(findCompatibleDevice=True,
         device=None,
         device_count=None,
         log_device_placement=True,
         allow_soft_placement=True,
         gpu_options_allow_growth=True):
    if tfVer == 2:
        tf.disable_v2_behavior()

    tfconfig = tf.ConfigProto(device_count=device_count)
    tfconfig.log_device_placement = log_device_placement
    tfconfig.allow_soft_placement = allow_soft_placement
    tfconfig.gpu_options.allow_growth = gpu_options_allow_growth

    UnetModelManager().defaultTFConfig = tfconfig
    UnetModelManager().defaultDevice = device

    if findCompatibleDevice is not None:
        devList = tfDevLib.list_local_devices()

        gpuMemoryLimit = 0
        gpuCudaMajor = 0
        gpuCudaMinor = 0
        gpuName = ""

        for x in devList:
            print("\nDevice:")
            print(x)
            if x.device_type == 'GPU':
                p = x.physical_device_desc.find("capability:")
                mj, mn = x.physical_device_desc[p + 12:].split('.')
                mj = int(mj)
                mn = int(mn)
                if mj > gpuCudaMajor:
                    gpuCudaMajor = mj
                    gpuCudaMinor = mn
                    gpuName = x.name
                    gpuMemoryLimit = int(x.memory_limit)
                elif (mj == gpuCudaMajor):
                    if mn > gpuCudaMinor:
                        gpuCudaMinor = mn
                        gpuName = x.name
                        gpuMemoryLimit = int(x.memory_limit)
                    elif mn == gpuCudaMinor:
                        if gpuMemoryLimit < int(x.memory_limit):
                            gpuName = x.name
                            gpuMemoryLimit = int(x.memory_limit)

        UnetModelManager().defaultDevice = "/device:CPU:0" if gpuName == "" \
            else gpuName

    print("\nDevice selected:", gpuName)


@SingletonDecorator
class UnetModelManager:
    def __init__(self):
        self._tfconfig = tf.ConfigProto()
        self._tfconfig.log_device_placement = True
        self._tfconfig.allow_soft_placement = True
        self._tfconfig.gpu_options.allow_growth = True

        self._device = None

        self._modelDict = dict()
        for file in models_path.glob('*'):
            if file.is_dir():
                self.addModel(file.name, file / 'config.yaml')

    def addModel(self, name, model):
        self._modelDict[name] = model

    def getModel(self, modelName):
        if not isinstance(modelName, str):
            raise TypeError("String expected")

        return self._modelDict.get(modelName, None)

    def getModelNames(self):
        return self._modelDict.keys()

    @property
    def defaultTFConfig(self):
        return self._tfconfig

    @defaultTFConfig.setter
    def defaultTFConfig(self, value):
        if not isinstance(value, tf.ConfigProto):
            raise TypeError("ConfigProto expected")

        self._tfconfig = value

    @property
    def defaultDevice(self):
        return self._device

    @defaultDevice.setter
    def defaultDevice(self, value):
        self._device = value


class UnetEvaluator():
    def __init__(self, modelName=None, img=None):
        self._mm = UnetModelManager()
        config_file_path = self._mm.getModel(modelName)
        self.config = YAMLConfig(config_file_path)

        self._model = self.get_model(self.config)(self.config)
        self.model_weight_path = str(config_file_path.parent) + "/"

        self.img = img


    def get_model(self, configuration):
        network_type = configuration.get_entry(['Network', 'type'], False) or '3DUNetDeep'

        if network_type == 'VNet':
            return VNet
        elif network_type == '3DUNetDeep':
            return UNet3DDeep
        elif network_type == '3DUNet':
            return UNet3D
        else:
            raise ValueError(
                'Network type "{}" not supported, use one of: [VNet, 3DUNetDeep, 3DUNet]'.format(network_type))

    @property
    def name(self):
        return self._model.name

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, value):
        # !todo:control de errores. No se comprueba el formato de la imagen
        if value is None:
            self._img = None
            self._outputShape = (0, 0, 0)
        else:
            # todo: No me acaba de gustar este roll (baja prioridad)
            self._img = np.rollaxis(value, 0, 3)
            # if self._model.standarizeImg: self._standarizeImg()
            # if self._model.standarizeSet: self._standarizeSet()
            #
            # self._adjustImgToPatchSize()
            # self._outputShape = self._img.shape  # aquí se sabe el tamaño de la salida
            # self._addBordersToImg()

        self._pred = None

    @img.setter
    def pred(self, value):
        self._pred = value

    @property
    def nPatches(self):
        # todo: este control de errores es muy básico
        if self._img is None:
            return 0

        sp = np.array(self._model.patchSize)
        si = np.array(self._outputShape)

        return np.prod(np.ceil(si / sp), dtype=int)

    @property
    def prediction(self):
        return self._pred

    # =============================================================================
    #     #!Todo: 1. En los recores de la imagen deberíamos coger le tamaño minimo
    #                y luego descartar lo que no se use
    #             2. Poner la información de contexto del borde a 0
    # =============================================================================
    def infer(self):
        seed = self.config.get_entry(['Training', 'seed'])
        # Seeds for reproducibility
        tf.random.set_random_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        # Parse the configuration file
        use_mixed_precision = self.config.get_entry(['Network', 'mixed_precision'])
        if use_mixed_precision:
            mixed_precision.experimental.set_policy('mixed_float16')
        model_load_path = self.model_weight_path
        self._model.load_weights(model_load_path)
        print('Loaded saved model from {}'.format(model_load_path))
        trainer = Tester(self.config, self._model)
        self.pred = trainer.infer(self.img)


class Tester:
    def __init__(self, configuration: YAMLConfig, model: Model):
        self.num_classes = configuration.get_entry(['Data', 'num_classes'])
        self.model_save_path = configuration.get_entry(['Output', 'model_save_path'])
        self.input_size = configuration.get_entry(['Network', 'input_size'])
        self.output_size = configuration.get_entry(['Network', 'output_size'])
        self.input_d = configuration.get_entry(['Network', 'input_depth'])
        self.output_d = configuration.get_entry(['Network', 'output_depth'])
        self.batch_size = configuration.get_entry(['Test', 'batch_size'])
        self.output_image_path = Path(configuration.get_entry(['Test', 'images_output_path']))

        self.output_image_path.mkdir(parents=True, exist_ok=True)
        self.model = model

    def infer(self, image_stack):
        image_stack = image_stack / 4095
        # image_stack = np.transpose(image_stack, axes=[1, 2, 0])

        input_height = self.input_size
        input_width = self.input_size
        input_depth = self.input_d
        output_height = self.output_size
        output_width = self.output_size
        output_channels = self.output_d

        height, width, channels = image_stack.shape
        padding_l = int((input_width - output_width) / 2)
        padding_t = int((input_height - output_height) / 2)
        padding_r = int((input_width - output_width) / 2)
        padding_b = int((input_height - output_height) / 2)
        padding_s = int(math.ceil((input_depth - output_channels) / 2))
        padding_e = int(math.ceil((input_depth - output_channels) / 2))

        padded_width = width + padding_l + padding_r
        padded_height = height + padding_t + padding_b
        padded_channels = channels + padding_s + padding_e
        padded_img = np.pad(image_stack, [(padding_t, padding_b), (padding_l, padding_r), (padding_s, padding_e)],
                            mode='constant')

        start_w_index = np.array(list(range(padding_l, padded_width - padding_r - self.output_size,
                                            self.output_size)) + [padded_width - padding_r - self.output_size])
        start_h_index = np.array(list(range(padding_t, padded_height - padding_b - self.output_size,
                                            self.output_size)) + [padded_height - padding_b - self.output_size])
        start_c_index = np.array(list(range(padding_s, padded_channels - padding_e - self.output_d, self.output_d))
                                 + [padded_channels - padding_e - self.output_d])

        rows_idx = np.tile(np.repeat(start_h_index, start_w_index.shape[0]), start_c_index.shape[0])
        cols_idx = np.tile(start_w_index, start_h_index.shape[0] * start_c_index.shape[0])
        channels_idx = np.repeat(start_c_index, start_w_index.shape[0] * start_h_index.shape[0])

        start_output_idx = np.array(list(zip(rows_idx, cols_idx, channels_idx)))
        end_output_idx = start_output_idx + [self.output_size, self.output_size, self.output_d]
        start_input_idx = start_output_idx - [padding_t, padding_l, padding_s]
        end_input_idx = start_input_idx + [self.input_size, self.input_size, self.input_d]

        prediction_img = np.zeros_like(padded_img)

        iterator = tqdm(zip(start_output_idx, end_output_idx, start_input_idx, end_input_idx),
                        total=start_output_idx.shape[0])
        # for i, (soi, eoi, sii, eii) in enumerate(iterator):
        #     image_patch = padded_img[sii[0]:eii[0], sii[1]:eii[1], sii[2]:eii[2]]
        #     prediction_img[soi[0]:eoi[0], soi[1]:eoi[1], soi[2]:eoi[2]] = self.model.test_iteration(
        #         image_patch[None, :, :, :, None])[0, :, :, :, 0]

        for i, (soi, eoi, sii, eii) in enumerate(iterator):
            image_patch = padded_img[sii[0]:eii[0], sii[1]:eii[1], sii[2]:eii[2]]
            prediction_img[soi[0]:eoi[0], soi[1]:eoi[1], soi[2]:eoi[2]] = self.model.test_iteration(
                image_patch[None, :, :, :, None])[0, :, :, :, 0]

        prediction_img = prediction_img[padding_t: padding_t + height, padding_l: padding_l + width,
                         padding_s:padding_s + channels]
        prediction_img = np.rollaxis(prediction_img, -1, 0)

        return prediction_img
