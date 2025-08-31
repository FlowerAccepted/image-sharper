import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt

class ImageSharpener(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.image = None
        self.sharpened_image = None

    def initUI(self):
        self.setWindowTitle('Image Sharpener')
        layout = QVBoxLayout()

        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.imageLabel)

        loadButton = QPushButton('Load Image', self)
        loadButton.clicked.connect(self.loadImage)
        layout.addWidget(loadButton)

        sharpenButton = QPushButton('Sharpen Image', self)
        sharpenButton.clicked.connect(self.sharpenImage)
        layout.addWidget(sharpenButton)

        saveButton = QPushButton('Save Image', self)
        saveButton.clicked.connect(self.saveImage)
        layout.addWidget(saveButton)

        self.setLayout(layout)
        self.resize(400, 400)

    def loadImage(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp)")
        if fileName:
            self.image = cv2.imread(fileName)
            self.displayImage(self.image)
            self.sharpened_image = None

    def sharpenImage(self):
        if self.image is not None:
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            self.sharpened_image = cv2.filter2D(self.image, -1, kernel)
            self.displayImage(self.sharpened_image)

    def saveImage(self):
        if self.sharpened_image is not None:
            fileName, _ = QFileDialog.getSaveFileName(self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg *.jpeg);;All Files (*)")
            if fileName:
                cv2.imwrite(fileName, self.sharpened_image)

    def displayImage(self, img):
        qformat = QImage.Format_RGB888
        outImage = QImage(img.data, img.shape[1], img.shape[0], img.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        pixmap = QPixmap.fromImage(outImage)
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageSharpener()
    ex.show()
    sys.exit(app.exec_())
