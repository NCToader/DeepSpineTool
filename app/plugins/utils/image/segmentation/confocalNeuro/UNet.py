from typing import Union

import tensorflow as tf
from tensorflow.python.keras import Model, Input
from tensorflow.keras.layers import Conv3D, MaxPool3D, Dropout, Conv3DTranspose
from tensorflow.keras.initializers import TruncatedNormal, VarianceScaling
from tensorflow.keras.regularizers import l2
from tensorflow.python.keras.layers import PReLU

from app.plugins.utils.segmentation.parser import YAMLConfig
import numpy as np


class SegModel(Model):
    def __init__(self, configuration: YAMLConfig):
        super().__init__()
        self.kernel_init = configuration.get_entry(['Network', 'kernel_init'])
        self.kernel_reg = configuration.get_entry(['Network', 'kernel_reg'])
        self.base_filt = configuration.get_entry(['Network', 'base_filt'])
        self.pad = configuration.get_entry(['Network', 'pad'])
        self.use_dropout = configuration.get_entry(['Network', 'droput'])
        self.dropout_prob = configuration.get_entry(['Network', 'droput_probability'])
        self.num_classes = configuration.get_entry(['Data', 'num_classes'])
        self.activation_function = configuration.get_entry(['Network', 'activation_function'])
        self.print_shapes = configuration.get_entry(['Output', 'print_shapes'])
        self.d_weight = configuration.get_entry(['Data', 'd_weight'], False)
        self.use_weights = configuration.get_entry(['Data', 'use_class_weights'], False)
        self.use_mixed_precision = configuration.get_entry(['Network', 'mixed_precision'])
        self.loss_type = configuration.get_entry(['Network', 'loss_type'])

        if self.d_weight:
            self.weight_method = configuration.get_entry(['Data', 'weight_method', 'type'])

        if self.use_weights:
            self.class_weights = configuration.get_entry(['Data', 'class_weights'])
            self.weighted_loss = tf.reshape(tf.constant(self.class_weights), [1, 1, 1, 1, self.num_classes])

        if self.kernel_init == 'normal':
            self.base_init = TruncatedNormal(stddev=0.1)
        elif self.kernel_init == 'He':
            self.base_init = VarianceScaling()

        self.reg_init = None
        if self.kernel_reg == 'l2':
            self.reg_factor = configuration.get_entry(['Network', 'reg_factor'])
            self.reg_init = l2(l2=self.reg_factor)

        self.padding = 'same' if self.pad else 'valid'
        self.dropout = Dropout(rate=self.dropout_prob)

    def conv_batch_relu(self, filters, kernel: Union[int, list, tuple] = (3, 3, 3),
                        stride: Union[int, list, tuple] = (1, 1, 1), name=None):

        conv = Conv3D(filters, kernel_size=kernel, strides=stride, padding=self.padding,
                      kernel_initializer=self.base_init, kernel_regularizer=self.reg_init,
                      activation=self.activation_function, name=name)
        return conv

    def upconvolve(self, filters, kernel: Union[int, list, tuple] = 2, stride: Union[int, list, tuple] = 2, name=None):
        conv = Conv3DTranspose(filters, kernel_size=kernel, strides=stride, padding=self.padding,
                               kernel_initializer=self.base_init, kernel_regularizer=self.reg_init, name=name)
        return conv

    def centre_crop_and_concat(self, prev_conv, up_conv):
        # If concatenating two different sized Tensors, centre crop the first Tensor to the right size and concat
        # Needed if you don't have padding
        p_c_s = prev_conv.shape
        u_c_s = up_conv.shape
        if self.pad and p_c_s[1] > u_c_s[1]:
            up_conv_padded = tf.pad(up_conv, [[0, 0], [1, 0], [1, 0], [1, 0], [0, 0]], 'CONSTANT')
            up_concat = tf.concat((prev_conv, up_conv_padded), 4)
        else:
            offsets = np.array([0, (p_c_s[1] - u_c_s[1]) // 2, (p_c_s[2] - u_c_s[2]) // 2,
                                (p_c_s[3] - u_c_s[3]) // 2, 0], dtype=np.int32)
            size = np.array([-1, u_c_s[1], u_c_s[2], u_c_s[3], p_c_s[4]], np.int32)
            prev_conv_crop = tf.slice(prev_conv, offsets, size)
            up_concat = tf.concat((prev_conv_crop, up_conv), 4)
        return up_concat

    def model(self, shape):
        x = Input(shape=shape)
        return Model(inputs=[x], outputs=self.call(x))

    def compute_loss(self, network_out, labels_one_hot, dweights=None, training=True):
        if self.loss_type == 'dice':
            probabilities = tf.nn.softmax(network_out)
            if training and self.use_weights:
                numerator = 2 * tf.reduce_sum(self.weighted_loss[0, 0, 0, 0] *
                                              tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3)), axis=1)
                denominator = tf.reduce_sum(self.weighted_loss[0, 0, 0, 0] *
                                            tf.reduce_sum(labels_one_hot + probabilities, axis=(1, 2, 3)), axis=1)
            else:
                numerator = 2 * tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3, 4))
                denominator = tf.reduce_sum(labels_one_hot + probabilities, axis=(1, 2, 3, 4))

            loss = 1 - tf.reduce_mean(numerator / denominator)
            print('{} / {}'.format(numerator, denominator))
        elif self.loss_type == 'dice_squared':
            # skip the batch and class axis for calculating Dice score
            probabilities = tf.nn.softmax(network_out)
            if training and self.use_weights:
                numerator = 2 * tf.reduce_sum(self.weighted_loss[0, 0, 0, 0] *
                                              tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3)), axis=1)
                denominator = tf.reduce_sum(self.weighted_loss[0, 0, 0, 0] *
                                            tf.reduce_sum((labels_one_hot ** 2) + (probabilities ** 2), axis=(1, 2, 3)),
                                            axis=1)
            else:
                numerator = 2 * tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3, 4))
                denominator = tf.reduce_sum((labels_one_hot ** 2) + (probabilities ** 2), axis=(1, 2, 3, 4))

            loss = 1 - tf.reduce_mean(numerator / denominator)
        elif self.loss_type == 'dice_vnet':
            probabilities = tf.nn.softmax(network_out)
            weights = 1 / (tf.reduce_sum(labels_one_hot, axis=(1, 2, 3)) ** 2)
            weights = tf.where(tf.math.is_inf(weights), -1, weights)
            weights = tf.where(weights == -1, tf.math.reduce_max(weights), weights)
            numerator = 2 * tf.reduce_sum(weights * tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3)),
                                          axis=1)
            denominator = tf.reduce_sum(weights * tf.reduce_sum(labels_one_hot + probabilities, axis=(1, 2, 3)),
                                        axis=1)
            loss = 1 - tf.reduce_mean(numerator / denominator)
        elif self.loss_type == 'dice_vnet2':
            probabilities = tf.nn.softmax(network_out)
            weights = 1 / (tf.reduce_sum(labels_one_hot, axis=(1, 2, 3)) ** 2)
            weights = tf.where(tf.math.is_inf(weights), 1, weights)
            numerator = 2 * tf.reduce_sum(weights * tf.reduce_sum(labels_one_hot * probabilities, axis=(1, 2, 3)),
                                          axis=1)
            denominator = tf.reduce_sum(weights * tf.reduce_sum(labels_one_hot + probabilities, axis=(1, 2, 3)),
                                        axis=1)
            loss = 1 - tf.reduce_mean(numerator / denominator)
        else:
            # TODO: consider sparse_softmax_cross_entropy_with_logits
            ce_loss = tf.nn.softmax_cross_entropy_with_logits(logits=network_out, labels=labels_one_hot)

            if training:
                if self.d_weight:
                    ce_loss = tf.multiply(ce_loss, dweights)

                if self.use_weights and self.loss_type == 'cross_entropy':
                    weighted_one_hot = tf.reduce_sum(self.weighted_loss * labels_one_hot, axis=-1)
                    ce_loss = ce_loss * weighted_one_hot
                else:

                    if self.d_weight:
                        if self.weight_method == 'window':
                            num_class_pixels = tf.stack(
                                [tf.reduce_sum(labels_one_hot[b_index][dweights[b_index] > 0], axis=0) for b_index
                                 in range(dweights.shape[0])])
                        else:
                            num_class_pixels = tf.stack(
                                [tf.reduce_sum(labels_one_hot[b_index][dweights[b_index] >= 0.01], axis=0) for b_index
                                 in range(dweights.shape[0])])
                    else:
                        num_class_pixels = tf.reduce_sum(labels_one_hot, axis=(1, 2, 3))

                    # norm_num_class_pixels = tf.where(num_class_pixels == 0,
                    #                                  tf.reduce_max(num_class_pixels, axis=-1, keepdims=True),
                    #                                  num_class_pixels)
                    # weights = tf.reduce_min(norm_num_class_pixels, axis=-1, keepdims=True) / norm_num_class_pixels
                    # weights = weights / tf.reduce_sum(weights, axis=-1, keepdims=True)
                    weights = tf.math.log((2 * tf.reduce_sum(num_class_pixels, -1, keepdims=True)) / num_class_pixels)
                    weights = tf.where(weights < 1, 1, weights)
                    weights = tf.where(tf.math.is_inf(weights), 0, weights)
                    weights = weights / tf.reduce_sum(weights, axis=-1, keepdims=True)

                    weight_map = tf.reduce_sum(
                        tf.reshape(weights, [labels_one_hot.shape[0], 1, 1, 1, self.num_classes]) * labels_one_hot,
                        axis=-1)

                    # if self.d_weight:
                    #     weight_map = weight_map.numpy()
                    #     if self.weight_method == 'window':
                    #         weight_map[dweights <= 0] = 0
                    #     else:
                    #         weight_map[dweights <= 0.01] = 0

                    ce_loss = ce_loss * weight_map

            loss = tf.reduce_mean(ce_loss)

        return loss

    def train_iteration(self, data, optimizer):
        dweights = None
        if self.d_weight:
            images, labels, dweights = data
        else:
            images, labels = data

        labels_one_hot = tf.squeeze(tf.one_hot(labels, self.num_classes, axis=-1), axis=-2)
        with tf.GradientTape() as tape:
            out = self(images, training=True)
            loss = self.compute_loss(out, labels_one_hot, dweights)
            if self.use_mixed_precision:
                scaled_loss = loss
                loss = optimizer.get_scaled_loss(loss)

        gradients = tape.gradient(loss, self.trainable_variables)
        if self.use_mixed_precision:
            gradients = optimizer.get_unscaled_gradients(gradients)
            loss = scaled_loss
        predictions = tf.expand_dims(tf.argmax(out, axis=-1), -1)

        return gradients, loss.numpy(), predictions.numpy()

    def validation_iteration(self, data):
        dweights = None
        if self.d_weight:
            images, labels, dweights = data
        else:
            images, labels = data

        labels_one_hot = tf.squeeze(tf.one_hot(labels, self.num_classes, axis=-1), axis=-2)
        out = self(images, training=True)
        loss = self.compute_loss(out, labels_one_hot, dweights, training=True)
        predictions = tf.expand_dims(tf.argmax(out, axis=-1), -1)

        return loss.numpy(), predictions.numpy()

    def test_iteration(self, image_stack):
        out = self(image_stack, training=False)
        predictions = tf.expand_dims(tf.argmax(out, axis=-1), -1)

        return predictions.numpy()


class UNet3D(SegModel):
    def __init__(self, configuration: YAMLConfig):
        super().__init__(configuration)

        self.conv_0_1 = self.conv_batch_relu(self.base_filt, name='conv_0_1')
        self.conv_0_2 = self.conv_batch_relu(self.base_filt * 2, name='conv_0_2')
        self.max_0_1 = MaxPool3D(2, 2, name='max_0_1')

        # Level one
        self.conv_1_1 = self.conv_batch_relu(self.base_filt * 2, name='conv_1_1')
        self.conv_1_2 = self.conv_batch_relu(self.base_filt * 4, name='conv_1_2')
        self.max_1_2 = MaxPool3D(2, 2, name='max_1_2')

        # Level two
        self.conv_2_1 = self.conv_batch_relu(self.base_filt * 4, name='conv_2_1')
        self.conv_2_2 = self.conv_batch_relu(self.base_filt * 8, name='conv_2_2')
        self.max_2_3 = MaxPool3D(2, 2, name='max_2_3')

        # Level three
        self.conv_3_1 = self.conv_batch_relu(self.base_filt * 8, name='conv_3_1')
        self.conv_3_2 = self.conv_batch_relu(self.base_filt * 16, name='conv_3_2')

        # Level two
        self.up_conv_3_4 = self.upconvolve(self.base_filt * 16, kernel=2, stride=2, name='up_conv_3_4')
        self.conv_4_1 = self.conv_batch_relu(self.base_filt * 8, name='conv_4_1')
        self.conv_4_2 = self.conv_batch_relu(self.base_filt * 8, name='conv_4_2')

        # Level one
        self.up_conv_4_5 = self.upconvolve(self.base_filt * 8, kernel=2, stride=2, name='up_conv_4_5')
        self.conv_5_1 = self.conv_batch_relu(self.base_filt * 4, name='conv_5_1')
        self.conv_5_2 = self.conv_batch_relu(self.base_filt * 4, name='conv_5_2')

        # Level zero
        self.up_conv_5_6 = self.upconvolve(self.base_filt * 4, kernel=2, stride=2, name='up_conv_5_6')
        self.conv_6_1 = self.conv_batch_relu(self.base_filt * 2, name='conv_6_1')
        self.conv_6_2 = self.conv_batch_relu(self.base_filt * 2, name='conv_6_2')

        self.conv_out = Conv3D(self.num_classes, 1, 1, padding='same', name='conv_out', dtype='float32')

    def call(self, inputs, training=None, mask=None):
        out = self.conv_0_1(inputs)
        conv_0_2 = self.conv_0_2(out)
        out = self.max_0_1(conv_0_2)

        out = self.conv_1_1(out)
        conv_1_2 = self.conv_1_2(out) if not self.use_dropout else self.dropout(self.conv_1_2(out), training)
        out = self.max_1_2(conv_1_2)

        out = self.conv_2_1(out)
        conv_2_2 = self.conv_2_2(out) if not self.use_dropout else self.dropout(self.conv_2_2(out), training)
        out = self.max_2_3(conv_2_2)

        out = self.conv_3_1(out)
        out = self.conv_3_2(out) if not self.use_dropout else self.dropout(self.conv_3_2(out), training)
        up_conv_3_4 = self.up_conv_3_4(out)

        out = self.centre_crop_and_concat(conv_2_2, up_conv_3_4)
        out = self.conv_4_1(out)
        out = self.conv_4_2(out) if not self.use_dropout else self.dropout(self.conv_4_2(out), training)

        up_conv_4_5 = self.up_conv_4_5(out)
        out = self.centre_crop_and_concat(conv_1_2, up_conv_4_5)
        out = self.conv_5_1(out)
        out = self.conv_5_2(out) if not self.use_dropout else self.dropout(self.conv_5_2(out), training)

        up_conv_5_6 = self.up_conv_5_6(out)
        out = self.centre_crop_and_concat(conv_0_2, up_conv_5_6)
        out = self.conv_6_1(out)
        out = self.conv_6_2(out) if not self.use_dropout else self.dropout(self.conv_6_2(out), training)

        out = self.conv_out(out)

        return out


class UNet3DDeep(SegModel):
    def __init__(self, configuration: YAMLConfig):
        super().__init__(configuration)

        shallow_n_nstride = [2, 2, 1]

        self.conv_0_1 = self.conv_batch_relu(self.base_filt, name='conv_0_1')
        self.conv_0_2 = self.conv_batch_relu(self.base_filt * 2, name='conv_0_2')
        self.max_0_1 = MaxPool3D(2, shallow_n_nstride, name='max_0_1')

        # Level one
        self.conv_1_1 = self.conv_batch_relu(self.base_filt * 2, name='conv_1_1')
        self.conv_1_2 = self.conv_batch_relu(self.base_filt * 4, name='conv_1_2')
        self.max_1_2 = MaxPool3D(2, shallow_n_nstride, name='max_1_2')

        # Level two
        self.conv_2_1 = self.conv_batch_relu(self.base_filt * 4, name='conv_2_1')
        self.conv_2_2 = self.conv_batch_relu(self.base_filt * 8, name='conv_2_2')
        self.max_2_3 = MaxPool3D(2, 2, name='max_2_3')

        # Level three
        self.conv_3_1 = self.conv_batch_relu(self.base_filt * 8, name='conv_3_1')
        self.conv_3_2 = self.conv_batch_relu(self.base_filt * 16, name='conv_3_2')
        self.max_3_4 = MaxPool3D(2, 2, name='max_3_4')

        # level four
        self.conv_4_1 = self.conv_batch_relu(self.base_filt * 16, name='conv_4_1')
        self.conv_4_2 = self.conv_batch_relu(self.base_filt * 32, name='conv_4_2')

        # level three
        self.up_conv_4_5 = self.upconvolve(self.base_filt * 32, kernel=2, stride=2, name='up_conv_4_5')
        self.conv_5_1 = self.conv_batch_relu(self.base_filt * 16, name='conv_5_1')
        self.conv_5_2 = self.conv_batch_relu(self.base_filt * 16, name='conv_5_2')

        # Level two
        self.up_conv_5_6 = self.upconvolve(self.base_filt * 16, kernel=2, stride=2, name='up_conv_5_6')
        self.conv_6_1 = self.conv_batch_relu(self.base_filt * 8, name='conv_6_1')
        self.conv_6_2 = self.conv_batch_relu(self.base_filt * 8, name='conv_6_2')

        # Level one
        self.up_conv_6_7 = self.upconvolve(self.base_filt * 8, kernel=2, stride=shallow_n_nstride, name='up_conv_6_7')
        self.conv_7_1 = self.conv_batch_relu(self.base_filt * 4, name='conv_7_1')
        self.conv_7_2 = self.conv_batch_relu(self.base_filt * 4, name='conv_7_2')

        # Level zero
        self.up_conv_7_8 = self.upconvolve(self.base_filt * 4, kernel=2, stride=shallow_n_nstride, name='up_conv_7_8')
        self.conv_8_1 = self.conv_batch_relu(self.base_filt * 2, name='conv_8_1')
        self.conv_8_2 = self.conv_batch_relu(self.base_filt * 2, name='conv_8_2')

        self.conv_out = Conv3D(self.num_classes, 1, 1, padding='same', name='conv_out', dtype='float32')

    def call(self, inputs, training=None, mask=None):
        out = self.conv_0_1(inputs)
        conv_0_2 = self.conv_0_2(out)
        out = self.max_0_1(conv_0_2)

        out = self.conv_1_1(out)
        conv_1_2 = self.conv_1_2(out) if not self.use_dropout else self.dropout(self.conv_1_2(out), training)
        out = self.max_1_2(conv_1_2)

        out = self.conv_2_1(out)
        conv_2_2 = self.conv_2_2(out) if not self.use_dropout else self.dropout(self.conv_2_2(out), training)
        out = self.max_2_3(conv_2_2)

        out = self.conv_3_1(out)
        conv_3_2 = self.conv_3_2(out) if not self.use_dropout else self.dropout(self.conv_3_2(out), training)
        out = conv_3_2

        out = self.max_3_4(out)
        out = self.conv_4_1(out)
        out = self.conv_4_2(out) if not self.use_dropout else self.dropout(self.conv_4_2(out), training)

        up_conv_4_5 = self.up_conv_4_5(out)
        out = self.centre_crop_and_concat(conv_3_2, up_conv_4_5)
        out = self.conv_5_1(out)
        out = self.conv_5_2(out) if not self.use_dropout else self.dropout(self.conv_5_2(out), training)

        up_conv_5_6 = self.up_conv_5_6(out)
        out = self.centre_crop_and_concat(conv_2_2, up_conv_5_6)
        out = self.conv_6_1(out)
        out = self.conv_6_2(out) if not self.use_dropout else self.dropout(self.conv_6_2(out), training)

        up_conv_6_7 = self.up_conv_6_7(out)
        out = self.centre_crop_and_concat(conv_1_2, up_conv_6_7)
        out = self.conv_7_1(out)
        out = self.conv_7_2(out) if not self.use_dropout else self.dropout(self.conv_7_2(out), training)

        up_conv_7_8 = self.up_conv_7_8(out)
        out = self.centre_crop_and_concat(conv_0_2, up_conv_7_8)
        out = self.conv_8_1(out)
        out = self.conv_8_2(out) if not self.use_dropout else self.dropout(self.conv_8_2(out), training)

        out = self.conv_out(out)

        return out


class VNet(SegModel):
    def __init__(self, configuration: YAMLConfig):
        super().__init__()
        self.kernel_init = configuration.get_entry(['Network', 'kernel_init'])
        self.kernel_reg = configuration.get_entry(['Network', 'kernel_reg'])
        self.base_filt = configuration.get_entry(['Network', 'base_filt'])
        self.pad = configuration.get_entry(['Network', 'pad'])
        self.use_dropout = configuration.get_entry(['Network', 'droput'])
        self.dropout_prob = configuration.get_entry(['Network', 'droput_probability'])
        self.num_classes = configuration.get_entry(['Data', 'num_classes'])
        self.activation_function = configuration.get_entry(['Network', 'activation_function'])
        self.print_shapes = configuration.get_entry(['Output', 'print_shapes'])
        self.d_weight = configuration.get_entry(['Data', 'd_weight'], False)
        self.use_weights = configuration.get_entry(['Data', 'use_class_weights'])
        self.use_mixed_precision = configuration.get_entry(['Network', 'mixed_precision'])
        self.loss_type = configuration.get_entry(['Network', 'loss_type'])
        self.ks = configuration.get_entry(['Network', 'kernel_size'])

        if self.use_weights:
            self.class_weights = configuration.get_entry(['Data', 'class_weights'])
            self.weighted_loss = tf.reshape(tf.constant(self.class_weights), [1, 1, 1, 1, self.num_classes])

        if self.kernel_init == 'normal':
            self.base_init = TruncatedNormal(stddev=0.1)
        elif self.kernel_init == 'He':
            self.base_init = VarianceScaling()

        if self.kernel_reg == 'l2':
            self.reg_init = l2(l2=0.1)

        self.padding = 'same' if self.pad else 'valid'
        self.dropout = Dropout(rate=self.dropout_prob)

        self.conv1_1 = Conv3D(self.base_filt, kernel_size=self.ks, strides=1, padding='same', name='conv1_1',
                              kernel_initializer=self.base_init)
        self.down_conv_1 = Conv3D(self.base_filt * 2, kernel_size=2, strides=2, padding='valid', name='dconv1',
                                  kernel_initializer=self.base_init)
        self.prelu1_1 = PReLU()
        self.dprelu1 = PReLU()

        self.conv2_1 = Conv3D(self.base_filt * 2, kernel_size=self.ks, strides=1, padding='same', name='conv2_1',
                              kernel_initializer=self.base_init)
        self.down_conv_2 = Conv3D(self.base_filt * 4, kernel_size=2, strides=2, padding='valid', name='dconv2',
                                  kernel_initializer=self.base_init)
        self.prelu2_1 = PReLU()
        self.dprelu2 = PReLU()

        self.conv3_1 = Conv3D(self.base_filt * 4, kernel_size=self.ks, strides=1, padding='same', name='conv3_1',
                              kernel_initializer=self.base_init)
        self.conv3_2 = Conv3D(self.base_filt * 4, kernel_size=self.ks, strides=1, padding='same', name='conv3_2',
                              kernel_initializer=self.base_init)
        self.down_conv_3 = Conv3D(self.base_filt * 8, kernel_size=2, strides=2, padding='valid', name='dconv3',
                                  kernel_initializer=self.base_init)
        self.prelu3_1 = PReLU()
        self.prelu3_2 = PReLU()
        self.dprelu3 = PReLU()

        self.conv4_1 = Conv3D(self.base_filt * 8, kernel_size=self.ks, strides=1, padding='same', name='conv4_1',
                              kernel_initializer=self.base_init)
        self.conv4_2 = Conv3D(self.base_filt * 8, kernel_size=self.ks, strides=1, padding='same', name='conv4_2',
                              kernel_initializer=self.base_init)
        self.conv4_3 = Conv3D(self.base_filt * 8, kernel_size=self.ks, strides=1, padding='same', name='conv4_3',
                              kernel_initializer=self.base_init)
        self.down_conv_4 = Conv3D(self.base_filt * 16, kernel_size=2, strides=2, padding='valid', name='dconv4',
                                  kernel_initializer=self.base_init)
        self.prelu4_1 = PReLU()
        self.prelu4_2 = PReLU()
        self.prelu4_3 = PReLU()
        self.dprelu4 = PReLU()

        self.conv5_1 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv5_1',
                              kernel_initializer=self.base_init)
        self.prelu5_1 = PReLU()
        self.conv5_2 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv5_2',
                              kernel_initializer=self.base_init)
        self.prelu5_2 = PReLU()
        self.conv5_3 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv5_3',
                              kernel_initializer=self.base_init)
        self.prelu5_3 = PReLU()

        self.up_conv_1 = Conv3DTranspose(self.base_filt * 8, kernel_size=2, strides=2, padding='valid', name='uconv1',
                                         kernel_initializer=self.base_init)
        self.conv6_1 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv6_1',
                              kernel_initializer=self.base_init)
        self.conv6_2 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv6_2',
                              kernel_initializer=self.base_init)
        self.conv6_3 = Conv3D(self.base_filt * 16, kernel_size=self.ks, strides=1, padding='same', name='conv6_3',
                              kernel_initializer=self.base_init)
        self.uprelu1 = PReLU()
        self.prelu6_1 = PReLU()
        self.prelu6_2 = PReLU()
        self.prelu6_3 = PReLU()

        self.up_conv_2 = Conv3DTranspose(self.base_filt * 4, kernel_size=2, strides=2, padding='valid', name='uconv2',
                                         kernel_initializer=self.base_init)
        self.conv7_1 = Conv3D(self.base_filt * 8, kernel_size=self.ks, strides=1, padding='same', name='conv7_1',
                              kernel_initializer=self.base_init)
        self.conv7_2 = Conv3D(self.base_filt * 8, kernel_size=self.ks, strides=1, padding='same', name='conv7_2',
                              kernel_initializer=self.base_init)
        self.uprelu2 = PReLU()
        self.prelu7_1 = PReLU()
        self.prelu7_2 = PReLU()

        self.up_conv_3 = Conv3DTranspose(self.base_filt * 2, kernel_size=2, strides=2, padding='valid', name='uconv3',
                                         kernel_initializer=self.base_init)
        self.conv8_1 = Conv3D(self.base_filt * 4, kernel_size=self.ks, strides=1, padding='same', name='conv8_1',
                              kernel_initializer=self.base_init)
        self.uprelu3 = PReLU()
        self.prelu8_1 = PReLU()

        self.up_conv_4 = Conv3DTranspose(self.base_filt, kernel_size=2, strides=2, padding='valid', name='uconv4',
                                         kernel_initializer=self.base_init)
        self.conv9_1 = Conv3D(self.base_filt * 2, kernel_size=self.ks, strides=1, padding='same', name='conv9_1',
                              kernel_initializer=self.base_init)
        self.conv9_2 = Conv3D(self.num_classes, kernel_size=self.ks, strides=1, padding='same', name='conv9_2',
                              kernel_initializer=self.base_init)
        self.uprelu4 = PReLU()
        self.prelu9_1 = PReLU()
        self.prelu9_2 = PReLU()

        self.conv_out = Conv3D(self.num_classes, 1, 1, padding='same', name='conv_out',
                               kernel_initializer=self.base_init)

    def call(self, inputs, training=None, mask=None):

        out = self.conv1_1(inputs)
        out1_1 = self.prelu1_1(out + inputs)

        out_down_conv_1 = self.dprelu1(self.down_conv_1(out1_1))
        out = self.conv2_1(out_down_conv_1)
        out_down_conv_1 = self.conv2_1(out_down_conv_1 + out)

        out_down_conv_2 = self.dprelu2(self.down_conv_2(out_down_conv_1))
        out = self.prelu3_1(self.conv3_1(out_down_conv_2))
        out = self.conv3_2(out)
        out_down_conv_2 = self.prelu3_2(out_down_conv_2 + out)

        out_down_conv_3 = self.dprelu3(self.down_conv_3(out_down_conv_2))
        out = self.prelu4_1(self.conv4_1(out_down_conv_3))
        out = self.prelu4_2(self.conv4_2(out))
        out = self.conv4_3(out)
        out_down_conv_3 = self.prelu4_3(out_down_conv_3 + out)

        out_down_conv_4 = self.dprelu4(self.down_conv_4(out_down_conv_3))
        out = self.prelu5_1(self.conv5_1(out_down_conv_4))
        out = self.prelu5_2(self.conv5_2(out))
        out = self.conv5_3(out)
        out_down_conv_4 = self.prelu5_3(out_down_conv_4 + out)

        up_conv_1 = self.uprelu1(self.up_conv_1(out_down_conv_4))
        concat_1 = tf.concat([out_down_conv_3, up_conv_1], axis=4)
        out = self.prelu6_1(self.conv6_1(concat_1))
        out = self.prelu6_2(self.conv6_2(out))
        out = self.conv6_3(out)
        out = self.prelu6_3(concat_1 + out)

        up_conv_2 = self.uprelu2(self.up_conv_2(out))
        concat_2 = tf.concat([out_down_conv_2, up_conv_2], axis=4)
        out = self.prelu7_1(self.conv7_1(concat_2))
        out = self.conv7_2(out)
        out = self.prelu7_2(concat_2 + out)

        up_conv_3 = self.uprelu3(self.up_conv_3(out))
        concat_3 = tf.concat([out_down_conv_1, up_conv_3], axis=4)
        out = self.conv8_1(concat_3)
        out = self.prelu8_1(concat_3 + out)

        up_conv_4 = self.uprelu4(self.up_conv_4(out))
        concat_4 = tf.concat([out1_1, up_conv_4], axis=4)
        out = self.conv9_1(concat_4)
        out = self.prelu9_1(concat_4 + out)
        out = self.prelu9_2(self.conv9_2(out))
        out = self.conv_out(out)

        return out
