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
#  This file is part of DeepSpineTool
#  Copyright (C) 2021 VG-Lab (Visualization & Graphics Lab), Universidad Rey Juan Carlos
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import threading

from tensorflow.python.keras import Model
from tqdm import tqdm
from pathlib import Path
from tensorflow.keras import mixed_precision
from app.plugins.utils.segmentation.parser import YAMLConfig
from app.plugins.utils.image.segmentation.confocalNeuro.UNet import UNet3D, UNet3DDeep, VNet
from tensorflow.python.client import device_lib as tfDevLib
from app.core.utils import SingletonDecorator
import math
import tensorflow as tf
import numpy as np
import random

models_path = Path(__file__).parent.parent.parent.parent.parent.parent.parent / 'models'


# https://www.tensorflow.org/guide/gpu

def set_seg_device(gpu_min_memory=6500):
    devList = tfDevLib.list_local_devices()
    last_gpu_ram = 0
    found_gpu = False
    found_gpu_with_enough_ram = False

    for x in devList:
        gpu_memory = int(x.memory_limit) / 1024 / 1024
        enough_ram = gpu_memory > gpu_min_memory

        if x.device_type == 'GPU':
            print('Found GPU: {} with {} MB of RAM, this device has {} RAM for the segmentation module.'
                  ''.format(x.name, gpu_memory, 'enough' if enough_ram else 'not enough'))

            found_gpu = True
            if gpu_memory > last_gpu_ram and enough_ram:
                UnetModelManager().GPU = x.name
                last_gpu_ram = gpu_memory
                found_gpu_with_enough_ram = True

    if not found_gpu:
        print('No GPU found, CPU will be used for the segmentation module.')
    elif not found_gpu_with_enough_ram:
        print('Found GPU, but it has not enough RAM to support our DL models, CPU will be used for the segmentation module.')


    UnetModelManager().CPU = tf.config.list_logical_devices('CPU')[0].name



    return found_gpu_with_enough_ram, found_gpu


@SingletonDecorator
class UnetModelManager:
    def __init__(self):
        self._GPU = None
        self._CPU = None

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
    def CPU(self):
        return self._CPU

    @CPU.setter
    def CPU(self, value):
        self._CPU = value

    @property
    def GPU(self):
        return self._GPU

    @GPU.setter
    def GPU(self, value):
        self._GPU = value


class UnetEvaluator:
    def __init__(self, modelName=None, img=None):
        self._mm = UnetModelManager()

        if self._mm.GPU is not None:
            self.device = self._mm.GPU
        else:
            self.device = self._mm.CPU

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
        tf.random.set_seed(seed)
        np.random.seed(seed)
        random.seed(seed)
        tf.random.set_global_generator = tf.random.Generator.from_seed(seed)
        # Parse the configuration file
        use_mixed_precision = self.config.get_entry(['Network', 'mixed_precision'])
        if use_mixed_precision:
            mixed_precision.experimental.set_policy('mixed_float16')
        model_load_path = self.model_weight_path
        self._model.load_weights(model_load_path).expect_partial()
        print('Loaded saved model from {}'.format(model_load_path))
        trainer = Tester(self.config, self._model)
        with tf.device(self.device):
            for progress in trainer.infer(self.img):
                yield progress
        self.pred = trainer.prediction_img


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
        image_stack = image_stack.astype(np.float32)
        image_stack -= image_stack.mean()
        image_stack /= image_stack.std()
        print('Callback, in thread %s' % threading.current_thread().name)

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

        for i, (soi, eoi, sii, eii) in enumerate(iterator):
            image_patch = padded_img[sii[0]:eii[0], sii[1]:eii[1], sii[2]:eii[2]]
            prediction_img[soi[0]:eoi[0], soi[1]:eoi[1], soi[2]:eoi[2]] = self.model.test_iteration(
                image_patch[None, :, :, :, None])[0, :, :, :, 0]

            yield 100 * i / (start_output_idx.shape[0] - 1)

        prediction_img = prediction_img[padding_t: padding_t + height, padding_l: padding_l + width,
                         padding_s:padding_s + channels]
        prediction_img = np.rollaxis(prediction_img, -1, 0)

        self.prediction_img = prediction_img

    def dense_infer(self, image_stack):
        image_stack = image_stack / image_stack.max()

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

        padding_ll = int((output_width / 2) / 2)
        padding_tt = int((output_height / 2) / 2)
        padding_rr = int((output_width / 2) / 2)
        padding_bb = int((output_height / 2) / 2)
        padding_ss = int((output_channels / 2) / 2)
        padding_ee = int((output_channels / 2) / 2)

        crop_output_size = self.output_size - padding_ll - padding_rr
        crop_d = self.output_d - padding_ss - padding_ee

        padded_width = width + padding_l + padding_r + padding_ll + padding_rr
        padded_height = height + padding_t + padding_b + padding_tt + padding_bb
        padded_channels = channels + padding_s + padding_e + padding_ss + padding_ee
        padded_img = np.pad(image_stack, [(padding_t + padding_tt, padding_b + padding_bb),
                                          (padding_l + padding_ll, padding_r + padding_rr),
                                          (padding_s + padding_ss, padding_e + padding_ee)],
                            mode='constant')

        start_w_index = np.array(list(
            range(padding_l + padding_ll,
                  padded_width - padding_r - padding_rr - self.output_size + padding_ll + padding_rr,
                  self.output_size - padding_ll - padding_rr)) + [
                                     padded_width - padding_r - padding_rr - self.output_size + padding_ll + padding_rr])
        start_h_index = np.array(list(
            range(padding_t + padding_tt,
                  padded_height - padding_b - padding_bb - self.output_size + padding_tt + padding_bb,
                  self.output_size - padding_tt - padding_bb)) + [
                                     padded_height - padding_b - padding_bb - self.output_size + padding_tt + padding_bb])
        start_c_index = np.array(list(
            range(padding_s + padding_ss,
                  padded_channels - padding_e - padding_ee - self.output_d + padding_ee + padding_ss,
                  self.output_d - padding_ss - padding_ee)) + [
                                     padded_channels - padding_e - padding_ee - self.output_d + padding_ee + padding_ss])

        rows_idx = np.tile(np.repeat(start_h_index, start_w_index.shape[0]), start_c_index.shape[0])
        cols_idx = np.tile(start_w_index, start_h_index.shape[0] * start_c_index.shape[0])
        channels_idx = np.repeat(start_c_index, start_w_index.shape[0] * start_h_index.shape[0])

        start_output_crop_idx = np.array(list(zip(rows_idx, cols_idx, channels_idx)))
        end_output_crop_idx = start_output_crop_idx + [self.output_size - padding_tt - padding_bb,
                                                       self.output_size - padding_ll - padding_rr,
                                                       self.output_d - padding_ss - padding_ee]
        start_output_idx = start_output_crop_idx - [padding_tt, padding_ll, padding_ss]
        end_output_idx = start_output_idx + [self.output_size, self.output_size, self.output_d]
        start_input_idx = start_output_idx - [padding_t, padding_l, padding_s]
        end_input_idx = start_input_idx + [self.input_size, self.input_size, self.input_d]

        prediction_img = np.zeros_like(padded_img)

        iterator = tqdm(
            zip(start_output_crop_idx, end_output_crop_idx, start_output_idx, end_output_idx, start_input_idx,
                end_input_idx),
            total=start_output_crop_idx.shape[0])

        for i, (soci, eoci, soi, eoi, sii, eii) in enumerate(iterator):
            image_patch = padded_img[sii[0]:eii[0], sii[1]:eii[1], sii[2]:eii[2]]
            prediction_img[soci[0]:eoci[0], soci[1]:eoci[1], soci[2]:eoci[2]] = self.model.test_iteration(
                image_patch[None, :, :, :, None])[0, padding_tt:padding_tt + crop_output_size,
                                                                                padding_ll:padding_ll + crop_output_size,
                                                                                padding_ss:padding_ss + crop_d, 0]
            yield 100 * i / (start_output_crop_idx.shape[0] - 1)

        prediction_img = prediction_img[padding_t + padding_tt: padding_t + padding_tt + height,
                         padding_l + padding_ll: padding_l + padding_ll + width,
                         padding_s + padding_ss:padding_s + padding_ss + channels]
        prediction_img = np.rollaxis(prediction_img, -1, 0)

        self.prediction_img = prediction_img
