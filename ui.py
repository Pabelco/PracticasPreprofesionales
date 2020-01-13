import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QAction, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot


from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np
#import pickle

#CATEGORIES = ["Geobacillus stearothermophilus", "Klebsiella aerogenes", "Micrococcus spp"]
CATEGORIES = ["Bacillus", "E.coli", "K.aerogenes", "Micrococcus", "P.aeruginosa", "S.aureus", "S.typhi", "Staphylococcus"]

IMG_SIZE = 50
#IMG_SIZE = 100

new_model = tf.keras.models.load_model('prueba.model')

class Ui_MainWindow(QWidget):
	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(474, 534)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
		self.gridLayout.setObjectName("gridLayout")
		spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
		self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setObjectName("pushButton")
		self.pushButton.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gridLayout.addWidget(self.pushButton, 0, 2, 1, 1)

		#Definiendo las proporciones de la pantalla
		self.gridLayout.setRowStretch(5, 1)
		self.gridLayout.setColumnStretch(2, 2)
		self.gridLayout.setColumnStretch(1, 7)
		self.gridLayout.setColumnStretch(0, 2)

		self.pushButton.clicked.connect(self.file_open)

		openFile = QAction('&Abrir imagen', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Abrir imagen')
		openFile.triggered.connect(self.file_open)


		self.bacterium_name = QtWidgets.QLabel(self.centralwidget)
		self.bacterium_name.setSizeIncrement(QtCore.QSize(0, 0))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.bacterium_name.setFont(font)
		self.bacterium_name.setObjectName("bacterium_name")
		self.bacterium_name.setAlignment(QtCore.Qt.AlignCenter)
		self.bacterium_name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gridLayout.addWidget(self.bacterium_name, 4, 1, 1, 1)

		self.other_bacterium = QtWidgets.QLabel(self.centralwidget)
		self.other_bacterium.setText("")
		self.other_bacterium.setObjectName("other_bacterium")
		self.other_bacterium.setAlignment(QtCore.Qt.AlignCenter)
		self.other_bacterium.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gridLayout.addWidget(self.other_bacterium, 5, 1, 1, 1)

		self.other = QtWidgets.QLabel(self.centralwidget)
		self.other.setObjectName("other")
		self.gridLayout.addWidget(self.other, 5, 0, 1, 1)

		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setObjectName("label")
		self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
		spacerItem1 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		self.gridLayout.addItem(spacerItem1, 3, 1, 1, 1)
		spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
		self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
		self.label_3 = QtWidgets.QLabel(self.centralwidget)
		self.label_3.setText("")
		self.label_3.setPixmap(QtGui.QPixmap("Resultados/Logo.png"))
		self.label_3.setObjectName("label_3")
		self.label_3.setAlignment(QtCore.Qt.AlignCenter)
		self.label_3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 21))
		self.menubar.setObjectName("menubar")
		self.menuArchivo = QtWidgets.QMenu(self.menubar)
		self.menuArchivo.setObjectName("menuArchivo")
		MainWindow.setMenuBar(self.menubar)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		self.actionAbrir = QtWidgets.QAction(MainWindow)
		self.actionAbrir.setObjectName("actionAbrir")
		#self.menuArchivo.addAction(self.actionAbrir)
		self.menuArchivo.addAction(openFile)
		self.menubar.addAction(self.menuArchivo.menuAction())

		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)

	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Deep Bacterium"))
		MainWindow.setWindowIcon(QtGui.QIcon('icon.png'))
		self.label.setText(_translate("MainWindow", "Abrir imagen..."))
		self.pushButton.setText(_translate("MainWindow", "Abrir"))
		self.bacterium_name.setText(_translate("MainWindow", "Nombre de la bacteria identificada"))
		self.other.setText(_translate("MainWindow", "Otros:"))
		self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
		self.actionAbrir.setText(_translate("MainWindow", "Abrir imagen"))

	def file_open(self):
		name, _ = QFileDialog.getOpenFileName(self, 'Abrir imagen', options=QFileDialog.DontUseNativeDialog)

		if not name:
			return

		X = []
		img_array = cv2.imread(name ,cv2.IMREAD_COLOR)

		height = img_array.shape[0]
		width = img_array.shape[1]

		for j in range(6):
			for i in range(8):
				crop_img = img_array[i*height//8:(i+1)*height//8, j*width//6:(j+1)*width//6]

				new_array = cv2.resize(crop_img, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
				X.append(new_array)

		X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
		

		'''
		pickle_in = open("X.pickle","rb")
		X_train = pickle.load(pickle_in)

		datagen = ImageDataGenerator(
			featurewise_center=True,				#Setea la media del dataset a 0
			featurewise_std_normalization=True,)		#Normaliza con desviacion estandard (divide cada input para su desviacion estandard
		datagen.fit(X_train)
		'''

		X = X.astype('float32')
		X_final = X/255.0
		#X_final = datagen.standardize(X)

		predictions = new_model.predict([X_final])

		probs = {}
		for i in range(len(predictions)):
			for j in range(len(predictions[i])):
				if j in probs:
					probs[j] += predictions[i][j]
				else:
					probs[j] = predictions[i][j]
				if i == len(predictions)-1:
					probs[j] /= len(predictions[i])
		probs = [[k, v*100/sum(probs.values())] for k, v in sorted(probs.items(), reverse=True, key=lambda item: item[1])]
		#result = np.argmax(predictions[0])
		result = probs[0][0]
		self.bacterium_name.setText(CATEGORIES[result]+' '+"{0:.2f}".format(probs[0][1])+' %')
		self.label_3.setPixmap(QtGui.QPixmap("Resultados/"+str(result)+".jpg"))

		self.other_bacterium.setText('')
		for i in range(1,len(probs)):
			separator = ''
			if self.other_bacterium.text() != '':
				separator = ', '
			self.other_bacterium.setText(self.other_bacterium.text()+separator+CATEGORIES[probs[i][0]]+' '+"{0:.2f}".format(probs[i][1])+' %')

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
