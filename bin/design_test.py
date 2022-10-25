import sys
import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QFileDialog
from converter_window import *
import image_converter
import sqlite3


DIGIT_TO_CHAR = {"1": "one",
                 "2": "two",
                 "3": "three",
                 "4": "four",
                 "5": "five",
                 "6": "six",
                 "7": "seven",
                 "8": "eight",
                 "9": "nine",
                 "0": "zero"}


def convert_to_binary_data(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData


def write_to_file(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")


def insert_blob(image_file, image_title=None):
    try:
        print("Connected to SQLite...")
        sqlite_connection = sqlite3.connect('ascii_images.db')
        cursor = sqlite_connection.cursor()
        print("SQLite connected")
        sqlite_insert_blob_query = """ INSERT INTO images
                                           (title, image, type) VALUES (?, ?, ?)"""

        image_type = image_file[image_file.rfind(".") + 1::]
        image = convert_to_binary_data(image_file)
        # Convert data into tuple format
        data_tuple = (image_title, image, image_type)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        sqlite_connection.commit()
        print("Image and file inserted successfully as a BLOB into a table")
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("SQLite connection is closed")


def read_blob_data():
    try:
        print("Connected to SQLite...")
        sqlite_connection = sqlite3.connect('ascii_images.db')
        cursor = sqlite_connection.cursor()
        print("SQLite connected")

        sql_fetch_blob_query = """SELECT * FROM images"""
        cursor.execute(sql_fetch_blob_query)
        record = cursor.fetchall()
        for row in record:
            title = row[1]
            image = row[2]
            image_type = row[3]

            print("Storing images on disk \n")
            image_path = "outputs/" + title + f".{image_type}"
            write_to_file(image, image_path)

        print("Clearing database")
        cursor.execute("DELETE FROM images")
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to insert blob data into sqlite table:", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("SQLite connection is closed")


class MyWidget(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        QMainWindow.__init__(self)
        uic.loadUi("converter_window.ui", self)
        self.btn_loadImage.clicked.connect(self.transform)
        self.btn_watchImages.clicked.connect(read_blob_data)

    def transform(self):
        file_path = QFileDialog.getOpenFileName(self, '')[0]
        img_data = image_converter.image_to_text(file_path)
        image_name = file_path[file_path.rfind("/") + 1:file_path.rfind("."):]
        for k in DIGIT_TO_CHAR.keys():
            image_name = image_name.replace(k, DIGIT_TO_CHAR[k])
        if type(img_data) is not list:
            img_data.save("temp.png")
            insert_blob("temp.png", image_name)
            os.remove("temp.png")
        else:
            img_data[0].save(f"temp.gif",
                             save_all=True, append_images=img_data[1:],
                             optimize=False, duration=10, loop=0)
            insert_blob("temp.gif", image_name)
            os.remove("temp.gif")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
