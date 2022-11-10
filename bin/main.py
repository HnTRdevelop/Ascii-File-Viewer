import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from main_window import *
import image_converter
import view_image
from PIL import Image


exts = Image.registered_extensions()
ALLOWED_TYPES = {ex for ex, f in exts.items() if f in Image.OPEN}


class MyWidget(Ui_main_window, QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        uic.loadUi("MainWindow.ui", self)

        self.files_list = []

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.update_files_list()

        self.widget_list.itemClicked.connect(self.open_file)

    def transform_image(self, file_path):
        image_name = file_path[file_path.rfind("/") + 1:file_path.rfind("."):]
        image_data = image_converter.image_to_ascii_art(file_path, True, True)
        print("Done!\n")
        view_image.display_image(image_data, image_name)

    def open_file(self, file):
        file_text = file.text()
        if os.path.isdir(f"{self.current_path}/{file_text}"):
            self.change_dir(file_text[::])
        else:
            self.transform_image(f"{self.current_path}/{file_text}")

    def change_dir(self, newdir):
        if newdir == "../":
            self.current_path = self.current_path[:self.current_path.rfind("/"):]
        else:
            self.current_path += f"/{newdir[:-1:]}"
        self.update_files_list()

    def update_files_list(self):
        self.clear_files()

        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.current_path):
            files.extend(dirnames)
            files.extend(filenames)
            break

        self.add_file("..", True)
        for file in files:
            isdir = os.path.isdir(f"{self.current_path}/{file}")
            if not isdir:
                file_extension = file[file.rfind(".")::]
                if file_extension not in ALLOWED_TYPES:
                    continue
            else:
                file += "/"
            self.add_file(file, False)

        for file_frame in self.files_list:
            self.widget_list.addItem(file_frame)

    def clear_files(self):
        self.widget_list.clear()
        self.files_list.clear()

    def add_file(self, name, isdir):
        if isdir:
            name += "/"
        self.files_list.append(name)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
