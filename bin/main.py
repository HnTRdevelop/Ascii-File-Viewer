import sys
import os
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from main_window import *
import image_converter
import image_viewer
from PIL import Image


extensions = Image.registered_extensions()
ALLOWED_IMAGE_TYPES = {ex for ex, f in extensions.items() if f in Image.OPEN}
ALLOWED_SOUND_TYPES = {".wav"}
del extensions


class FileWidget(QWidget):
    def __init__(self, parent, file_name, file_type, widget_id, current_path):
        super().__init__(parent)

        self.file_name = file_name
        self.file_type = file_type

        self.setMaximumSize(QtCore.QSize(16777215, 64))
        self.setStyleSheet("background-color: rgb(222, 221, 218);")
        self.setObjectName(f"file_widget{widget_id}")
        file_widget_layout = QtWidgets.QGridLayout(self)
        file_widget_layout.setObjectName(f"file_widget_layout{widget_id}")
        file_widget_img = QtWidgets.QLabel(self)
        file_widget_img.setMinimumSize(QtCore.QSize(46, 46))
        file_widget_img.setMaximumSize(QtCore.QSize(46, 46))

        if self.file_type == "dir":
            img = QPixmap("images/dir.png")
        elif self.file_type == "image":
            img = QPixmap(f"{current_path}/{self.file_name}")
        else:
            img = QPixmap("images/snd.png")

        file_widget_img.setPixmap(img)
        file_widget_img.setScaledContents(True)
        file_widget_img.setObjectName(f"file_widget_img{widget_id}")
        file_widget_layout.addWidget(file_widget_img, 0, 0, 1, 1)
        file_widget_name = QtWidgets.QLabel(self)
        file_widget_name.setObjectName(f"file_widget_name{widget_id}")
        file_widget_layout.addWidget(file_widget_name, 0, 1, 1, 1)

        file_widget_name.setText(file_name)

    def mousePressEvent(self, event):
        window.open_file(self.file_name)


def convert_image(file_path):
    image_name = file_path[file_path.rfind("/") + 1:file_path.rfind("."):]
    image_data = image_converter.image_to_ascii_art(file_path, True, True)
    image_viewer.display_image(image_data, image_name)


class MainWindow(Ui_main_window, QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        uic.loadUi("MainWindow.ui", self)

        self.action_move_back.triggered.connect(self.move_back)

        self.files_list = []

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path_line.setText(self.current_path)
        self.update_files_list()

    def open_file(self, file):
        if os.path.isdir(f"{self.current_path}/{file}") or file == "..":
            self.change_dir(file[::])
        else:
            file_extension = file[file.rfind(".")::]
            if file_extension in ALLOWED_IMAGE_TYPES:
                convert_image(f"{self.current_path}/{file}")
            else:
                # Заглушка для звуковых файлов
                pass

    def move_back(self):
        self.change_dir("..")

    def change_dir(self, newdir):
        if newdir == "..":
            self.current_path = self.current_path[:self.current_path.rfind("/"):]
        else:
            self.current_path += f"/{newdir}"
        self.update_files_list()
        self.current_path_line.setText(self.current_path)

    def update_files_list(self):
        self.clear_file_list()

        files = []
        for (dirpath, dirnames, filenames) in os.walk(self.current_path):
            files.extend(dirnames)
            files.extend(filenames)
            break

        self.add_file("..", "")
        for file in files:
            isdir = os.path.isdir(f"{self.current_path}/{file}")
            file_extension = ""
            if not isdir:
                file_extension = file[file.rfind(".")::]
                if (file_extension not in ALLOWED_IMAGE_TYPES) and (file_extension not in ALLOWED_SOUND_TYPES):
                    continue
            self.add_file(file, file_extension)

        for file_widget in self.files_list:
            self.scroll_area_layout.addWidget(file_widget)

    def clear_file_list(self):
        for file_widget in self.files_list:
            file_widget.deleteLater()

        self.files_list.clear()

    def add_file(self, name, extension):
        file_type = "sound"
        if extension == "":
            file_type = "dir"
        elif extension in ALLOWED_IMAGE_TYPES:
            file_type = "image"

        file_widget = FileWidget(self.scroll_area_widget, name, file_type, len(self.files_list), self.current_path)
        self.files_list.append(file_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
