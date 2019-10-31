import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D

from tensorflow.keras.utils import normalize
# example of using ImageDataGenerator to normalize images
#from keras.datasets import mnist

import pickle
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from tqdm import tqdm

import random

IMG_SIZE = 50




def create_training_data():
	DATADIR = "./"

	CATEGORIES = ["Acinetobacter.baumanii", "Actinomyces.israeli", "Bacteroides.fragilis", "Bifidobacterium.spp", "Escherichia.coli"]

	training_data = []

	for category in CATEGORIES:

		path = os.path.join(DATADIR,category)  # path
		class_num = CATEGORIES.index(category)  # get the classification  (0 or a 1). 0=baumanii 1=israeli

		for img in tqdm(os.listdir(path)):  # iterate over each image
			try:
				img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_COLOR)  # convert to array
				new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
				training_data.append([new_array, class_num])  # add this to our training_data
			except Exception as e:  # in the interest in keeping the output clean...
				print(e)
				pass
			#except OSError as e:
			#	print("OSErrroBad img most likely", e, os.path.join(path,img))
			#except Exception as e:
			#	print("general exception", e, os.path.join(path,img))

	# Si no se desordena mandaria primero todas las de una clase
	random.shuffle(training_data)

	X = []
	y = []

	for features,label in training_data:
		X.append(features)
		y.append(label)

	print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 3))

	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
	y = np.array(y)

	pickle_out = open("X.pickle","wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()

	pickle_out = open("y.pickle","wb")
	pickle.dump(y, pickle_out)
	pickle_out.close()

try:
	pickle_in = open("X.pickle","rb")
	X = pickle.load(pickle_in)

	pickle_in = open("y.pickle","rb")
	y = pickle.load(pickle_in)
except Exception as e:
	create_training_data() # Esto solo debe hacer la primera vez

	pickle_in = open("X.pickle","rb")
	X = pickle.load(pickle_in)

	pickle_in = open("y.pickle","rb")
	y = pickle.load(pickle_in)


X = X/255.0
#X = normalize(X, axis=-1, order=2)

#Data augmentation
datagen = ImageDataGenerator(
    featurewise_center=True,				#Setea la media del dataset a 0
    featurewise_std_normalization=True,		#Normaliza con desviacion estandard (divide cada input para su desviacion estandard)
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,)

datagen.fit(X)
it = datagen.flow(X, y, batch_size=10)




model = Sequential()

model.add(Conv2D(256, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())  # Convierte el feature maps 3D a un feature vectors 1D

model.add(Dense(64))
model.add(Activation('sigmoid'))

model.add(Dense(1))
model.add(Activation('sigmoid'))

model.compile(loss='binary_crossentropy',
			  optimizer='adam',
			  metrics=['accuracy'])

#Sin data augmentation
#model.fit(X, y, batch_size=10, epochs=5, validation_split=0.3)

#Con data augmentation
model.fit_generator(it, epochs=5, steps_per_epoch=2) #steps_per_epoch * batch_size = number_of_rows_in_train_data

#Guardar modelo
#model.save('prueba.model')

#Cargar modelo
#new_model = tf.keras.models.load_model('prueba.model')

#predictions = new_model.predict([X])

