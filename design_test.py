import sys

import math
import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QFileDialog
from PIL import Image, ImageFont, ImageDraw, ImageSequence


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("converter.ui", self)
        self.load_image.clicked.connect(self.transform)

    def transform(self):
        fname = QFileDialog.getOpenFileName(self, '')[0]
        Converter(fname)


class Converter:
    def __init__(self, image, invert=True):
        self.pallete = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "
        self.image = image
        self.second_image_name = image
        self.invert = invert
        self.FONT_SIZE = 15
        self.image_to_text(self.pallete, image, invert)

    def get_char(self, brightness, colors_table):
        step = 255 / len(colors_table)
        for i in range(1, len(colors_table) + 1):
            if i * step >= brightness:
                return colors_table[i - 1]

    def save_into_db(self, db_name, file_name1, file_name2):
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute(
            f'''insert into images(original) values("{file_name1}")
            '''
        )
        cur.execute(
            f'''update images
            set converted = "{file_name2}"
            where original = "{file_name1}"
            '''
        )
        con.commit()
        con.close()

    def image_to_text(self, colors_table, image_name, reverse):
        img = Image.open(image_name)

        extention = image_name[image_name.rfind(".") + 1::]

        if extention != "gif":
            size_factor = img.size[1] if img.size[1] > img.size[0] else img.size[0]
            if size_factor < 128:
                resize_factor = 1
            else:
                resize_factor = (15 * math.sqrt(size_factor - 128)) / math.sqrt(2560 - 128) + 1

            img = img.reduce(int(resize_factor))
            pixels = img.load()
            x, y = img.size

            output = Image.new("RGB", (x * self.FONT_SIZE, y * self.FONT_SIZE), (0, 0, 0))
            draw = ImageDraw.Draw(output)
            font = ImageFont.truetype("font.ttf", self.FONT_SIZE + 1)

            if reverse:
                colors_table = colors_table[::-1]

            for iy in range(y):
                for ix in range(x):
                    pixel = pixels[ix, iy]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                    brightness = (r + g + b) / 3
                    char = self.get_char(brightness, colors_table)
                    draw.text((ix * self.FONT_SIZE, iy * self.FONT_SIZE), char, (r, g, b, 255), font=font)

            self.save_into_db("ascii_images.db", self.second_image_name, image_name)
            name = image_name[image_name.rfind("/") + 1:]
            output.save(f"outputs/{name}")

            return 0

        else:
            if reverse:
                colors_table = colors_table[::-1]
            frames = []
            for frame in [frame.copy() for frame in ImageSequence.Iterator(img)]:
                pixels = 0

                size_factor = frame.size[1] if frame.size[1] > frame.size[0] else frame.size[0]
                if size_factor < 128:
                    resize_factor = 1
                else:
                    resize_factor = (15 * math.sqrt(size_factor - 128)) / math.sqrt(2560 - 128) + 1

                if frame.mode == "P":
                    continue
                frame = frame.reduce(int(resize_factor))
                pixels = frame.load()
                x, y = frame.size

                out = Image.new("RGB", (x * self.FONT_SIZE, y * self.FONT_SIZE), (0, 0, 0))
                draw = ImageDraw.Draw(out)
                font = ImageFont.truetype("font.ttf", self.FONT_SIZE + 1)

                for iy in range(y):
                    for ix in range(x):
                        pixel = pixels[ix, iy]
                        r = pixel[0]
                        g = pixel[1]
                        b = pixel[2]
                        brightness = (r + g + b) / 3
                        char = self.get_char(brightness, colors_table)
                        draw.text((ix * self.FONT_SIZE, iy * self.FONT_SIZE), char, (r, g, b, 255), font=font)

                frames.append(out)
            self.save_into_db("ascii_images.db", self.second_image_name, image_name)
            frames[0].save(f"outputs/{image_name[image_name.rfind('/') + 1:]}",
                           save_all=True, append_images=frames[1:],
                           optimize=False, duration=10, loop=0)

        return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())