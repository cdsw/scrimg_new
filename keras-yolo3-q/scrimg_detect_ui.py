import cv2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from scrimg_detect import *

class ScrimgDetect_UI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scrimg Detect")
        self.btn_upload = QPushButton("Upload Image")
        self.btn_detect = QPushButton("Detect")
        self.btn_reset = QPushButton("Reset")
        self.btn_save = QPushButton("Save")
        self.layout_buttons = QHBoxLayout()
        self.layout_buttons.addWidget(self.btn_upload)
        self.layout_buttons.addWidget(self.btn_detect)
        self.layout_buttons.addWidget(self.btn_reset)
        self.layout_buttons.addWidget(self.btn_save)
        self.label_input = QLabel()
        self.label_output = QLabel()
        self.empty = QPixmap("./utilities/empty.png")
        self.empty = self.empty.scaled(750,750)
        self.label_input.setPixmap(self.empty)
        self.label_output.setPixmap(self.empty)
        self.layout_images = QHBoxLayout()
        self.layout_images.addWidget(self.label_input)
        self.layout_images.addWidget(self.label_output)
        self.layout_main = QVBoxLayout()
        self.layout_main.addLayout(self.layout_buttons)
        self.layout_main.addLayout(self.layout_images)
        self.setLayout(self.layout_main)

        self.btn_upload.clicked.connect(self.upload)
        self.btn_detect.clicked.connect(self.detect)
        self.btn_detect.setEnabled(False)
        self.btn_reset.clicked.connect(self.clearh)
        self.btn_save.clicked.connect(self.saveto)
        self.btn_save.setEnabled(False)

        self.initializeScrimg()

    def initializeScrimg(self):
        version = 'T0515'
        grid = 8
        model_path = 'model_data/yolo-' + version + '.h5'
        anchors_path = 'model_data/scrimg_anchors-' + version + '.txt'
        classes_path = 'model_data/scrimg_classes.txt'
        threshold = 0.1
        iou = 0.35
        model_image_size = (32 * grid, 32 * grid)
        gpu_num = 1
        config_path = "./utilities/config.txt"
        path = "./dataset/output/"
        self.sc = ScrimgDetector(config_path, version, model_path, anchors_path, classes_path, threshold, iou,
                            model_image_size, gpu_num)

    # to test. Exception test: edge, node coverage
    def upload(self):
        self.inp_filename, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "Image Files (*.png *.jpg)")
        try:
            ph = QPixmap(self.inp_filename)
            self.label_input.setPixmap(ph.scaled(750,750))
            self.btn_detect.setEnabled(True)
            self.label_output.setPixmap(self.empty)
        except:
            print("Error reading image")
            QMessageBox.about(self, "Error", "Error reading image. Image not loaded.")
            self.btn_detect.setEnabled(False)

    # to test. Exception test: edge, node coverage
    def detect(self):
        try:
            self.out_filename = self.sc.detect_from_gui(self.inp_filename)
            ph = QPixmap(self.out_filename)
            self.label_output.setPixmap(ph.scaled(750, 750))
            self.btn_save.setEnabled(True)
        except:
            QMessageBox.about(self, "Error", "Error detecting image.")
            print("Error detecting image")

    def clearh(self):
        self.label_input.setPixmap(self.empty)
        self.label_output.setPixmap(self.empty)
        self.out_filename = ""
        self.btn_detect.setEnabled(False)
        self.btn_save.setEnabled(False)

    def saveto(self):
        fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","Image Files (*.png *.jpg)")
        if fileName != '':
            cv2.imwrite(fileName, cv2.imread(self.out_filename))
            QMessageBox.about(self, "Saved", "Image saved to " + fileName + ".")

if __name__ == "__main__":
    app = QApplication([])
    scrimg = ScrimgDetect_UI()
    scrimg.initializeScrimg()
    scrimg.show()
    app.exec()