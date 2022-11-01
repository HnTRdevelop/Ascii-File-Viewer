import sys
import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QFileDialog
from converter_window import *
import image_converter
import view_image


class MyWidget(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        uic.loadUi("converter_window.ui", self)
        self.btn_loadImage.clicked.connect(self.transform)

    def transform(self):
        file_path = QFileDialog.getOpenFileName(self, '')[0]
        image_name = file_path[file_path.rfind("/") + 1:file_path.rfind("."):]
        image_type = file_path[file_path.rfind(".") + 1::]

        image_data = image_converter.image_to_ascii_art(file_path, True)
        print("Done!\n")
        view_image.display_image(image_data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
