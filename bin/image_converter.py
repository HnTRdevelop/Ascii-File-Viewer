import math
from PIL import Image, ImageFont, ImageDraw, ImageSequence


FONT_SIZE = 15
TABLES = [
    " @",
    " .:-=+*#%@",
    " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
]
COLORS_TABLE = TABLES[2]


def get_char(brightness, error):
    b = brightness + error
    b = 255 if b > 255 else 0 if b < 0 else b

    step = len(COLORS_TABLE) / 255
    char = COLORS_TABLE[int(b * step) - 1]
    return char, brightness - COLORS_TABLE.index(char) / step


def get_resize_factor(size_x, size_y):
    size_factor = size_x if size_x > size_y else size_y
    resize_factor = 1
    if size_factor > 128:
        resize_factor = (16 * (size_factor - 128)) / 2594 + 1
    return resize_factor


def get_color_error(new_color, old_color):
    r = old_color[0] - new_color[0]
    g = old_color[1] - new_color[1]
    b = old_color[2] - new_color[2]
    return [r, g, b].copy()


def get_color(r, g, b, error):
    r = 255 if r + error[0] >= 128 else 0
    g = 255 if g + error[1] >= 128 else 0
    b = 255 if b + error[2] >= 128 else 0
    return r, g, b


def draw_char(pixel, brightness_error, color_error, draw, blending_mode, x, y, font):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    brightness = r * 0.299 + g * 0.587 + b * 0.114
    char, brightness_error = get_char(brightness, brightness_error)
    color = get_color(r, g, b, color_error)
    color_error = get_color_error(color, (r, g, b))
    if blending_mode:
        pass
    draw.text((x * FONT_SIZE, y * FONT_SIZE), char,
              color,
              font=font)
    return brightness_error, color_error.copy()


def image_to_text(image_path, blending_mode):
    img = Image.open(image_path)

    extension = image_path[image_path.rfind(".") + 1::]
    print(extension)

    if extension != "gif":
        print("Working with image...")
        resize_factor = get_resize_factor(img.size[0], img.size[1])

        img = img.reduce(int(resize_factor))
        pixels = img.load()
        x, y = img.size

        output = Image.new("RGB", (x * FONT_SIZE, y * FONT_SIZE), (0, 0, 0))
        draw = ImageDraw.Draw(output)
        font = ImageFont.truetype("font.ttf", FONT_SIZE + 1)

        for iy in range(y):
            brightness_error = 0
            color_error = [0, 0, 0]
            for ix in range(x):
                pixel = pixels[ix, iy]
                brightness_error, color_error = draw_char(pixel,
                                                          brightness_error, color_error,
                                                          draw,
                                                          blending_mode,
                                                          ix, iy,
                                                          font)

    # Working with gifs
    else:
        frames = []
        frame_id = 0
        for frame in [frame.copy() for frame in ImageSequence.Iterator(img)]:
            print(f"Working with frame {frame_id}...")
            frame_id += 1

            resize_factor = get_resize_factor(frame.size[0], frame.size[1])

            if frame.mode == "P":
                continue
            frame = frame.reduce(int(resize_factor))
            pixels = frame.load()
            x, y = frame.size

            out = Image.new("RGB", (x * FONT_SIZE, y * FONT_SIZE), (0, 0, 0))
            draw = ImageDraw.Draw(out)
            font = ImageFont.truetype("font.ttf", FONT_SIZE + 1)

            for iy in range(y):
                brightness_error = 0
                color_error = [0, 0, 0]
                for ix in range(x):
                    pixel = pixels[ix, iy]
                    brightness_error, color_error = draw_char(pixel,
                                                              brightness_error, color_error,
                                                              draw,
                                                              blending_mode,
                                                              ix, iy,
                                                              font)

            frames.append(out)
        output = frames.copy()

    img.close()
    return output
