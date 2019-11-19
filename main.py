import tensorflow as tf
from tensorflow.keras.datasets import cifar10
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D

from tensorflow.keras.utils import normalize

from tensorflow.keras import optimizers
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
IMG_SIZE = 100
#IMG_SIZE = 800
#IMG_SIZE_X = 600
#IMG_SIZE_Y = 800


def create_training_data():
	DATADIR = "./"

	CATEGORIES = ["Geobacillus.stearothermophilus", "Klebsiella.aerogenes", "Micrococcus.sp"]

	training_data = []
	training_data_test = []

	for category in CATEGORIES:
		
		path = os.path.join(DATADIR,category)  # path
		class_num = CATEGORIES.index(category)  # get the classification (0 or a 1...) 0=Geobacillus 1=Klebsiella...

		
		for img in tqdm(os.listdir(path)):  # iterate over each image
			try:
				img_array = cv2.imread(os.path.join(path,img) ,cv2.IMREAD_COLOR)  # convert to array

				height = img_array.shape[0]
				width = img_array.shape[1]

				for j in range(3):
					for i in range(4):
						crop_img = img_array[i*height//4:(i+1)*height//4, j*width//3:(j+1)*width//3]

						new_array = cv2.resize(crop_img, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
						training_data.append([new_array, class_num])  # add this to our training_data

						#cv2.imshow("cropped_"+str(i)+'_'+str(j), new_array)
			except Exception as e:  # in the interest in keeping the output clean...
				raise
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

	X_test = []
	y_test = []

	contador = 0
	for features,label in training_data:
		if contador < 0.2 * len(training_data):	#Agregando 20% de los datos para testing
			X_test.append(features)
			y_test.append(label)
		else:
			X.append(features)
			y.append(label)
		contador += 1

	#print(X[0].reshape(-1, IMG_SIZE, IMG_SIZE, 3))

	X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
	y = np.array(y)

	X_test = np.array(X_test).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
	y_test = np.array(y_test)

	pickle_out = open("X.pickle","wb")
	pickle.dump(X, pickle_out)
	pickle_out.close()

	pickle_out = open("y.pickle","wb")
	pickle.dump(y, pickle_out)
	pickle_out.close()

	pickle_out = open("X_test.pickle","wb")
	pickle.dump(X_test, pickle_out)
	pickle_out.close()

	pickle_out = open("y_test.pickle","wb")
	pickle.dump(y_test, pickle_out)
	pickle_out.close()

try:
	pickle_in = open("X.pickle","rb")
	X = pickle.load(pickle_in)

	pickle_in = open("y.pickle","rb")
	y = pickle.load(pickle_in)

	pickle_in = open("X_test.pickle","rb")
	X_test = pickle.load(pickle_in)

	pickle_in = open("y_test.pickle","rb")
	y_test = pickle.load(pickle_in)
except Exception as e:
	create_training_data() # Esto solo debe hacer la primera vez

	pickle_in = open("X.pickle","rb")
	X = pickle.load(pickle_in)

	pickle_in = open("y.pickle","rb")
	y = pickle.load(pickle_in)

	pickle_in = open("X_test.pickle","rb")
	X_test = pickle.load(pickle_in)

	pickle_in = open("y_test.pickle","rb")
	y_test = pickle.load(pickle_in)


X = X/255.0
#X = normalize(X, axis=-1, order=2)
X_test = X_test/255.0

#Data augmentation
datagen = ImageDataGenerator(
    featurewise_center=False,				#Setea la media del dataset a 0
    featurewise_std_normalization=False,		#Normaliza con desviacion estandard (divide cada input para su desviacion estandard)
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    horizontal_flip=True,
    vertical_flip=True,)

datagen_test = ImageDataGenerator(
    featurewise_center=False,				#Setea la media del dataset a 0
    featurewise_std_normalization=False,		#Normaliza con desviacion estandard (divide cada input para su desviacion estandard)
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True,)

datagen.fit(X)
it = datagen.flow(X, y, batch_size=2)

datagen_test.fit(X_test)
it_test = datagen.flow(X_test, y_test, batch_size=1)

#Para graficar las imagenes generadas por data Augmentation

for i in range(9):
	plt.subplot(330 + 1 + i)
	batch = it.next()
	image = batch[0][0] * 255.0	#Se multiplica por 255 porque antes se normalizo dividiendo para 255
	image = image.astype('uint8')
	plt.imshow(image)
plt.show()
############################################################
model = Sequential()

model.add(Conv2D(64, (3, 3), input_shape=X.shape[1:]))
model.add(Activation('relu'))
model.add(Dropout(0.25))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(128, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(256, (3, 3)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Flatten())  # Convierte el feature maps 3D a un feature vectors 1D



model.add(Dense(256))
model.add(Activation('relu'))

model.add(Dense(1))
model.add(Activation('relu'))




opt = optimizers.Adam(lr=0.0000001, decay=0.5 ,clipvalue=0.25)
model.compile(loss='binary_crossentropy',
			  optimizer=opt,
			  metrics=['accuracy'])

#Sin data augmentation
#model.fit(X, y, batch_size=10, epochs=5, validation_split=0.2)

#Con data augmentation
historia = model.fit_generator(it, epochs=20, steps_per_epoch=12, validation_data=it_test, validation_steps=28) #steps_per_epoch * batch_size = number_of_rows_in_train_data

#Guardar modelo
#model.save('prueba.model')

#Cargar modelo
#new_model = tf.keras.models.load_model('prueba.model')

#predictions = new_model.predict([X])


#############################################
#Graficar curvas de precicion y perdida
'''
accuracy = historia.history['accuracy']
val_accuracy = historia.history['val_accuracy']
loss = historia.history['loss']
val_loss = historia.history['val_loss']
epochs = range(len(accuracy))

plt.plot(epochs, accuracy, 'bo', label='Training accuracy')
plt.plot(epochs, val_accuracy, 'b', label='Validation accuracy')
plt.title('Training and validation accuracy')
plt.legend()
plt.figure()

plt.plot(epochs, loss, 'bo', label='Training loss')
plt.plot(epochs, val_loss, 'b', label='Validation loss')
plt.title('Training and validation loss')
plt.legend()

plt.show()
'''