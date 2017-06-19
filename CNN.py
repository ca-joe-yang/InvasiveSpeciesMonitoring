import sys
import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.advanced_activations import PReLU
from keras.layers.convolutional import Convolution2D, MaxPooling2D
from keras.optimizers import SGD, Adam, Adagrad
from keras.utils import np_utils, generic_utils
import IO

IMAGE_ROW = 128
IMAGE_COLUMN = 128
IMAGE_SIZE = IMAGE_ROW * IMAGE_COLUMN

train_images, train_labels = IO.load_train()
test_images = IO.load_test()

model = Sequential()

model.add(Convolution2D(32, (3, 3), activation='relu', input_shape=(IMAGE_ROW, IMAGE_COLUMN, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Convolution2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

print('Compiling model...')
model.compile(loss="binary_crossentropy", 
              optimizer="adam",
              metrics=["accuracy"])

print('Fitting model...')
model.fit(train_images,
          train_labels,
          batch_size=32, nb_epoch=10,    
          shuffle=True)

model.save('model/CNN.model')

result = model.predict(test_images,
                       batch_size=100, verbose=1)

IO.write_result(result, 'result/CNN.csv')
