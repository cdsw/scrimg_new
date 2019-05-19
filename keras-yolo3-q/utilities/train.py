"""
Retrain the YOLO model for your own dataset.
"""

import numpy as np
import keras.backend as K
from keras.layers import Input, Lambda
from keras.models import Model
from keras.optimizers import Adam
from keras.callbacks import TensorBoard, ModelCheckpoint, ReduceLROnPlateau, EarlyStopping

from utilities.yolo3.model import preprocess_true_boxes, tiny_yolo_body, yolo_loss
from utilities.yolo3.utils import get_random_data

class Trainer:
    def __init__(self, img_size, version, num_epoch_init, num_epoch_full, annotation_path, anchors_path, model_path,
                 log_dir='logs/', classes_path='model_data/scrimg_classes.txt'):
        self.annotation_path = annotation_path
        self.log_dir = log_dir
        self.version = version
        self.classes_path = classes_path
        self.anchors_path = anchors_path
        self.model_path = model_path
        self.class_names = self.get_classes()
        self.num_classes = len(self.class_names)
        self.anchors = self.get_anchors()
        self.input_shape = (img_size, img_size)  # multiple of 32, hw

        self.model = self.create_tiny_model(self.input_shape, self.anchors, self.num_classes,
                                            freeze_body=2, weights_path=self.model_path)
        self.logging = TensorBoard(log_dir=self.log_dir)
        self.checkpoint = ModelCheckpoint(self.log_dir + 'ep{epoch:03d}-loss{loss:.3f}-val_loss{val_loss:.3f}.h5',
                                     monitor='val_loss', save_weights_only=True, save_best_only=True, period=5)
        self.reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=3, verbose=1)
        self.early_stopping = EarlyStopping(monitor='val_loss', min_delta=0, patience=10, verbose=1)
        self.num_val, self.num_train, self.lines = self.randomize_annotations()
        self.num_epoch_init = num_epoch_init
        self.num_epoch_full = num_epoch_full + num_epoch_init

    def randomize_annotations(self):
        val_split = 0.1
        with open(self.annotation_path) as f:
            lines = f.readlines()
        np.random.seed(10101)
        np.random.shuffle(lines)
        np.random.seed(None)
        num_val = int(len(lines) * val_split)
        num_train = len(lines) - num_val
        return num_val, num_train, lines

    def train(self):
        # Train with frozen layers first, to get a stable loss.
        # Adjust num epochs to your dataset. This step is enough to obtain a not bad model.
        final_model_path = None
        if True:
            self.model.compile(optimizer=Adam(lr=1e-3), loss={
                # use custom yolo_loss Lambda layer.
                'yolo_loss': lambda y_true, y_pred: y_pred})

            batch_size = 32
            print('Train on {} samples, val on {} samples, with batch size {}.'.format(self.num_train, self.num_val, batch_size))
            self.model.fit_generator(
                self.data_generator_wrapper(self.lines[:self.num_train], batch_size, self.input_shape, self.anchors, self.num_classes),
                steps_per_epoch=max(1, self.num_train // batch_size),
                validation_data=self.data_generator_wrapper(self.lines[self.num_train:], batch_size, self.input_shape, self.anchors,
                                                       self.num_classes),
                validation_steps=max(1, self.num_val // batch_size),
                epochs=self.num_epoch_init,
                initial_epoch=0,
                callbacks=[self.logging, self.checkpoint])
            final_model_path = self.log_dir + 'init-yolo-' + self.version + '.h5'
            self.model.save_weights(final_model_path)


        # Unfreeze and continue training, to fine-tune.
        # Train longer if the result is not good.
        if True:
            for i in range(len(self.model.layers)):
                self.model.layers[i].trainable = True
            self.model.compile(optimizer=Adam(lr=1e-4),
                          loss={'yolo_loss': lambda y_true, y_pred: y_pred})  # recompile to apply the change
            print('Unfreeze all of the layers.')

            batch_size = 16  # note that more GPU memory is required after unfreezing the body
            print('Train on {} samples, val on {} samples, with batch size {}.'.format(self.num_train, self.num_val, batch_size))
            self.model.fit_generator(
                self.data_generator_wrapper(self.lines[:self.num_train], batch_size, self.input_shape, self.anchors, self.num_classes),
                steps_per_epoch=max(1, self.num_train // batch_size),
                validation_data=self.data_generator_wrapper(self.lines[self.num_train:], batch_size, self.input_shape, self.anchors,
                                                            self.num_classes),
                validation_steps=max(1, self.num_val // batch_size),
                epochs=self.num_epoch_full,
                initial_epoch=self.num_epoch_init,
                callbacks=[self.logging, self.checkpoint, self.reduce_lr, self.early_stopping])
            final_model_path = self.log_dir + 'final-yolo-' + self.version + '.h5'
            self.model.save_weights(final_model_path)
            #tfjs.converters.save_keras_model(self.model, 'E:/tfjs-----/')
        return final_model_path, self.log_dir

        # Further training if needed.

    def get_classes(self):
        '''loads the classes'''
        with open(self.classes_path) as f:
            class_names = f.readlines()
        class_names = [c.strip() for c in class_names]
        return class_names

    def get_anchors(self):
        '''loads the anchors from a file'''
        with open(self.anchors_path) as f:
            anchors = f.readline()
        anchors = [float(x) for x in anchors.split(',')]
        return np.array(anchors).reshape(-1, 2)

    def create_tiny_model(self, input_shape, anchors, num_classes, load_pretrained=True, freeze_body=2,
                          weights_path='model_data/tiny_yolo_weights.h5'):
        '''create the training model, for Tiny YOLOv3'''
        K.clear_session()  # get a new session
        image_input = Input(shape=(None, None, 3))
        h, w = input_shape
        num_anchors = len(anchors)

        y_true = [Input(shape=(h // {0: 32, 1: 16}[l], w // {0: 32, 1: 16}[l], \
                               num_anchors // 2, num_classes + 5)) for l in range(2)]

        model_body = tiny_yolo_body(image_input, num_anchors // 2, num_classes)
        print('Create Tiny YOLOv3 model with {} anchors and {} classes.'.format(num_anchors, num_classes))

        if load_pretrained:
            model_body.load_weights(weights_path, by_name=True, skip_mismatch=True)
            print('Load weights {}.'.format(weights_path))
            if freeze_body in [1, 2]:
                # Freeze the darknet body or freeze all but 2 output layers.
                num = (20, len(model_body.layers) - 2)[freeze_body - 1]
                for i in range(num): model_body.layers[i].trainable = False
                print('Freeze the first {} layers of total {} layers.'.format(num, len(model_body.layers)))

        model_loss = Lambda(yolo_loss, output_shape=(1,), name='yolo_loss',
                            arguments={'anchors': anchors, 'num_classes': num_classes, 'ignore_thresh': 0.7})(
            [*model_body.output, *y_true])
        model = Model([model_body.input, *y_true], model_loss)

        return model

    def data_generator(self, annotation_lines, batch_size, input_shape, anchors, num_classes):
        '''data generator for fit_generator'''
        n = len(annotation_lines)
        i = 0
        while True:
            image_data = []
            box_data = []
            for b in range(batch_size):
                if i == 0:
                    np.random.shuffle(annotation_lines)
                image, box = get_random_data(annotation_lines[i], input_shape, random=True)
                image_data.append(image)
                box_data.append(box)
                i = (i + 1) % n
            image_data = np.array(image_data)
            box_data = np.array(box_data)
            y_true = preprocess_true_boxes(box_data, input_shape, anchors, num_classes)
            yield [image_data, *y_true], np.zeros(batch_size)

    def data_generator_wrapper(self, annotation_lines, batch_size, input_shape, anchors, num_classes):
        n = len(annotation_lines)
        if n == 0 or batch_size <= 0: return None
        return self.data_generator(annotation_lines, batch_size, input_shape, anchors, num_classes)

#t = Trainer(256, 'T0516')
#t.train()