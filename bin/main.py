import sys
import os
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from main_window import *
import image_converter
import image_viewer
import sound_visualiser
from PIL import Image


extensions = Image.registered_extensions()
ALLOWED_IMAGE_TYPES = {ex for ex, f in extensions.items() if f in Image.OPEN}
ALLOWED_SOUND_TYPES = {".wav", ".mp3", ".ogg"}
del extensions


# Класс для виджета файла
class FileWidget(QWidget):
    def __init__(self, parent, file_name, file_type, widget_id, current_path):
        super().__init__(parent)

        # Сохраняем данные об картинке
        self.file_name = file_name
        self.file_type = file_type

        # Задаём максимальные размеры виджета
        self.setMaximumSize(QtCore.QSize(16777215, 128))

        # Задаём стиль виджета
        self.setStyleSheet("background-color: rgb(222, 221, 218);")

        # Устанавилваем има виджета
        self.setObjectName(f"file_widget{widget_id}")

        # Создаём layout виджета
        file_widget_layout = QtWidgets.QGridLayout(self)
        file_widget_layout.setObjectName(f"file_widget_layout{widget_id}")

        # Создаём изображение виджета
        file_widget_img = QtWidgets.QLabel(self)
        file_widget_img.setMinimumSize(QtCore.QSize(110, 110))
        file_widget_img.setMaximumSize(QtCore.QSize(110, 110))

        # Выбираем картинку для виджета
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

        # Создаём label виджета
        file_widget_name = QtWidgets.QLabel(self)
        file_widget_name.setObjectName(f"file_widget_name{widget_id}")
        file_widget_name.setText(file_name)
        file_widget_layout.addWidget(file_widget_name, 0, 1, 1, 1)

    # Открываем файл при нажатии на виджет
    def mousePressEvent(self, event):
        window.open_file(self.file_name)


class MainWindow(Ui_main_window, QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        uic.loadUi("MainWindow.ui", self)

        # Подключаем toolbar кнопки к их функциям
        self.action_move_back.triggered.connect(self.move_back)

        # Создаём список для виджетов
        self.files_list = []

        # Получаем путь до программы (нужно что-бы работало на всех os)
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.current_path_line.setText(self.current_path)

        # Обновляем список файлов
        self.update_files_list()

    # Функция для открытия файлов
    def open_file(self, file):
        # Если файл является директорией, то переходим в неё
        if os.path.isdir(f"{self.current_path}/{file}") or file == "..":
            self.change_dir(file[::])
        # Иначе октрываем файл соотвествующей функцией
        else:
            file_extension = file[file.rfind(".")::]
            if file_extension in ALLOWED_IMAGE_TYPES:
                image_data = image_converter.image_to_ascii_art(f"{self.current_path}/{file}", True, True)
                image_viewer.display_image(image_data, file)
            else:
                sound_visualiser.visualise_sound(f"{self.current_path}/{file}", file)

    # Функция возврата выше по пути
    def move_back(self):
        self.change_dir("..")

    # Функция для смены дериктории
    def change_dir(self, new_dir):
        if new_dir == "..":
            self.current_path = self.current_path[:self.current_path.rfind("/"):]
        else:
            self.current_path += f"/{new_dir}"
        self.update_files_list()
        self.current_path_line.setText(self.current_path)

    # Функция для обновления списка файлов
    def update_files_list(self):
        # Удаление устаревших виджетов
        self.clear_file_list()

        # Поулаем список файлов в директории
        files = []
        for (dir_paths, dir_names, filenames) in os.walk(self.current_path):
            files.extend(dir_names)
            files.extend(filenames)
            break

        # Добавляем директорию "../" (Директория возврата выше по пути)
        self.add_file("..", "")

        # Добавляем все файлы, которые может обработать программа
        for file in files:
            isdir = os.path.isdir(f"{self.current_path}/{file}")
            file_extension = ""
            if not isdir:
                file_extension = file[file.rfind(".")::]
                if (file_extension not in ALLOWED_IMAGE_TYPES) and (file_extension not in ALLOWED_SOUND_TYPES):
                    continue
            self.add_file(file, file_extension)

        # Отображаем виджеты
        for file_widget in self.files_list:
            self.scroll_area_layout.addWidget(file_widget)

    # Функция для удаления виджетов файлов
    def clear_file_list(self):
        # Удаляем виджеты файлов
        for file_widget in self.files_list:
            file_widget.deleteLater()

        # Очищение списка виждетов
        self.files_list.clear()

    # Функция для добавление виджета в список
    def add_file(self, name, extension):
        # Определяем тип файла
        file_type = "sound"
        if extension == "":
            file_type = "dir"
        elif extension in ALLOWED_IMAGE_TYPES:
            file_type = "image"

        # Создаём виджет
        file_widget = FileWidget(self.scroll_area_widget, name, file_type, len(self.files_list), self.current_path)

        # Добавляем виджет в список
        self.files_list.append(file_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    global window
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
