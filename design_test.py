import sys

import math
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
        self.invert = invert
        self.FONT_SIZE = 15
        self.image_to_text(self.pallete, image, invert)

    def get_char(self, brightness, colors_table):
        step = 255 / len(colors_table)
        for i in range(1, len(colors_table) + 1):
            if i * step >= brightness:
                return colors_table[i - 1]

    def image_to_text(self, colors_table, image_name, reverse):
        img = Image.open(image_name)

        extention = image_name[:image_name.rfind("."):]

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

        image_name = image_name[image_name.rfind(".") + 1:]
        name = image_name[image_name.rfind("/") + 1:]
        output.save(f"outputs/{name}.{extention}")

        return 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())