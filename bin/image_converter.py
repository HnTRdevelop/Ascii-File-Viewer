import math
from PIL import Image, ImageFont, ImageDraw, ImageSequence


FONT_SIZE = 15


def get_char(brightness):
    # colors_table = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    colors_table = " .:-=+*#%@"
    step = 255 / len(colors_table)
    for i in range(1, len(colors_table) + 1):
        if i * step >= brightness:
            return colors_table[i - 1]


def get_resize_factor(size_x, size_y):
    size_factor = size_x if size_x > size_y else size_y
    resize_factor = 1
    if size_factor > 128:
        resize_factor = (16 * (size_factor - 128)) / 2594.13 + 1
    return resize_factor


def get_color(r, g, b):
    clr = [r, g, b]
    if max(clr) < min(clr) + 32:
        return 255, 255, 255
    new_clr = [r, g, b]
    new_clr[clr.index(min(clr))] = 0
    clr.remove(min(clr))

    if min(clr) != 0:
        if max(clr) / min(clr) >= 1.25:
            new_clr[new_clr.index(min(clr))] = 0

    new_clr = [255 if i > 0 else 0 for i in new_clr]

    return new_clr[0], new_clr[1], new_clr[2]


def image_to_text(image_path):
    img = Image.open(image_path)

    extension = image_path[image_path.rfind(".") + 1::]
    print(extension)

    output = None

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
            for ix in range(x):
                pixel = pixels[ix, iy]
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                brightness = (r + g + b) / 3
                char = get_char(brightness)
                draw.text((ix * FONT_SIZE, iy * FONT_SIZE), char, get_color(r, g, b), font=font)

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
                for ix in range(x):
                    pixel = pixels[ix, iy]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                    brightness = (r + g + b) / 3
                    char = get_char(brightness)
                    draw.text((ix * FONT_SIZE, iy * FONT_SIZE), char, get_color(r, g, b), font=font)

            frames.append(out)
        output = frames.copy()

    img.close()
    return output
