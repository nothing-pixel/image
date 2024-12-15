#create the Easy Editor photo editor here!
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, 
                            QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QMessageBox)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

from PIL import Image
from PIL.ImageFilter import SHARPEN,BLUR,EMBOSS

#membuat jendela utama
app = QApplication([])
jendela = QWidget()
jendela.resize(700, 500)
jendela.setWindowTitle('Aplikasi Easy Editor')

#menambahkan widget
btn_dir = QPushButton('Folder')
list_file = QListWidget()
lb_image = QLabel('Image')

btn_left = QPushButton('Left')
btn_right = QPushButton('Right')
btn_mirror = QPushButton('Mirror')
btn_sharp = QPushButton('Sharpness')
btn_bw = QPushButton('Black/White')

#membuat layout
row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()

col1.addWidget(btn_dir)
col1.addWidget(list_file)
col2.addWidget(lb_image)

row_tools = QHBoxLayout()
row_tools.addWidget(btn_left)
row_tools.addWidget(btn_right)
row_tools.addWidget(btn_mirror)
row_tools.addWidget(btn_sharp)
row_tools.addWidget(btn_bw)

col2.addLayout(row_tools)
row.addLayout(col1, 20)
row.addLayout(col2, 80)

jendela.setLayout(row)

#menampilkan daftar title gambar
workdir = ''

def filter(files, extensions):
    result = []
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showFilenamesList():
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    chooseWorkdir()
    filenames = filter(os.listdir(workdir), extensions)

    list_file.clear()
    for filename in filenames:
        list_file.addItem(filename)

btn_dir.clicked.connect(showFilenamesList)

class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"
    
    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)
    
    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()
    
    def saveImage(self):
        path = os.path.join(self.dir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def bw(self):
        self.image = self.image.convert('L')
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)

    def tajam(self):
        self.image = self.image.filter(SHARPEN)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)

    def rotate(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)

    def kaca(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(self.dir, self.save_dir,self.filename)
        self.showImage(image_path)

def showChosenImage():
    if list_file.currentRow() >= 0:
        filename = list_file.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)

workimage = ImageProcessor()
list_file.currentRowChanged.connect(showChosenImage)

btn_bw.clicked.connect(workimage.bw)
btn_mirror.clicked.connect(workimage.kaca)
btn_left.clicked.connect(workimage.rotate)
btn_right.clicked.connect(workimage.rotate)
btn_sharp.clicked.connect(workimage.tajam)

jendela.show()
app.exec()

