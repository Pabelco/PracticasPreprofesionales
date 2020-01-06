import tensorflow as tf

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QAction
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import numpy as np

IMG_SIZE = 100

new_model = tf.keras.models.load_model('prueba.model')

class Ui_MainWindow(QWidget):
	def setupUi(self, MainWindow):
		

		MainWindow.setObjectName("MainWindow")
		MainWindow.resize(433, 449)
		self.centralwidget = QtWidgets.QWidget(MainWindow)
		self.centralwidget.setObjectName("centralwidget")
		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(22, 20, 261, 23))
		self.label.setObjectName("label")
		self.pushButton = QtWidgets.QPushButton(self.centralwidget)
		self.pushButton.setGeometry(QtCore.QRect(290, 20, 111, 23))
		self.pushButton.setObjectName("pushButton")

		#self.pushButton.clicked.connect(self.on_click)


		openFile = QAction('&Open File', self)
		openFile.setShortcut('Ctrl+O')
		openFile.setStatusTip('Open File')
		openFile.triggered.connect(self.file_open)


		self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
		self.graphicsView.setGeometry(QtCore.QRect(30, 130, 371, 221))
		self.graphicsView.setObjectName("graphicsView")
		self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
		self.progressBar.setGeometry(QtCore.QRect(30, 70, 381, 21))
		self.progressBar.setProperty("value", 24)
		self.progressBar.setObjectName("progressBar")
		self.label_2 = QtWidgets.QLabel(self.centralwidget)
		self.label_2.setGeometry(QtCore.QRect(110, 370, 241, 41))
		self.label_2.setSizeIncrement(QtCore.QSize(0, 0))
		font = QtGui.QFont()
		font.setPointSize(12)
		self.label_2.setFont(font)
		self.label_2.setObjectName("label_2")
		MainWindow.setCentralWidget(self.centralwidget)
		self.menubar = QtWidgets.QMenuBar(MainWindow)
		self.menubar.setGeometry(QtCore.QRect(0, 0, 433, 21))
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
		MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
		self.label.setText(_translate("MainWindow", "Abrir imagen..."))
		self.pushButton.setText(_translate("MainWindow", "Abrir"))
		self.label_2.setText(_translate("MainWindow", "Nombre de la bacteria identificada"))
		self.menuArchivo.setTitle(_translate("MainWindow", "Archivo"))
		self.actionAbrir.setText(_translate("MainWindow", "Abrir"))


	def file_open(self):
		# need to make name an tupple otherwise i had an error and app crashed
		name, _ = QFileDialog.getOpenFileName(self, 'Open File', options=QFileDialog.DontUseNativeDialog)

		if not name:
			return


		X = []
		img_array = cv2.imread(name ,cv2.IMREAD_COLOR)

		height = img_array.shape[0]
		width = img_array.shape[1]

		for j in range(3):
			for i in range(4):
				crop_img = img_array[i*height//4:(i+1)*height//4, j*width//3:(j+1)*width//3]

				new_array = cv2.resize(crop_img, (IMG_SIZE, IMG_SIZE))  # resize to normalize data size
				X.append(new_array)

		X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 3)
		X = X/255.0

		predictions = new_model.predict([X])
		print(predictions)
		#print(np.argmax(predictions[0]))

		#file = open(name, 'r')
		#self.editor()
		'''
		with file:
			text = file.read()
			self.textEdit.setText(text)
		'''

'''
class App(QWidget):
	def __init__(self):
		super().__init__()
		self.title = 'PyQt5 file dialogs - pythonspot.com'
		self.left = 10
		self.top = 10
		self.width = 640
		self.height = 480
		self.initUI()
	
	def initUI(self):
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		
		self.openFileNameDialog()
		self.openFileNamesDialog()
		self.saveFileDialog()
		
		self.show()
	
	def openFileNameDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
		if fileName:
			print(fileName)
	
	def openFileNamesDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		files, _ = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "","All Files (*);;Python Files (*.py)", options=options)
		if files:
			print(files)
	
	def saveFileDialog(self):
		options = QFileDialog.Options()
		options |= QFileDialog.DontUseNativeDialog
		fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
		if fileName:
			print(fileName)
'''
if __name__ == "__main__":
	import sys
	
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ui = Ui_MainWindow()
	ui.setupUi(MainWindow)
	MainWindow.show()
	sys.exit(app.exec_())
