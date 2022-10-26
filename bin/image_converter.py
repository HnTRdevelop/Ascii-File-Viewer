import math
from PIL import Image, ImageFont, ImageDraw, ImageSequence


FONT_SIZE = 15


def get_char(brightness):
    # colors_table = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/|()1{}[]?-_+~<>i!lI;:,\"^`'. "[::-1]
    colors_table = " .:-=+*#%@"
    step = len(colors_table) / 255
    return colors_table[int(brightness * step) - 1]


def get_resize_factor(size_x, size_y):
    size_factor = size_x if size_x > size_y else size_y
    resize_factor = 1
    if size_factor > 128:
        resize_factor = (19 * (size_factor - 128)) / 2594.13 + 1
    return resize_factor


def get_error(new_color, old_color):
    error = [old_color[0] - new_color[0],
             old_color[1] - new_color[1],
             old_color[2] - new_color[2]]
    return error


def get_color(r, g, b, error=[0, 0, 0]):
    r = 255 if r + error[0] > 128 else 0
    g = 255 if g + error[1] > 128 else 0
    b = 255 if b + error[2] > 128 else 0
    return r, g, b


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
            error = [0, 0, 0]
            for ix in range(x):
                pixel = pixels[ix, iy]
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                brightness = max([r, g, b])
                char = get_char(brightness)
                color = get_color(r, g, b, error)
                error = get_error(color, (r, g, b))
                draw.text((ix * FONT_SIZE, iy * FONT_SIZE), char, color, font=font)

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
