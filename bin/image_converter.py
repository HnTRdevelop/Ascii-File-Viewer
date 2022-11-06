from PIL import Image, ImageSequence


# HnTR - Gray levels tables, I think we need them, or not, idk
# " @"
# " .:-=+*#%@"
# " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
COLORS_TABLE = " .:-=+*#%@"
BLEND_MAP = [[0, 0, 0, 5, 3],
             [2, 4, 5, 4, 2],
             [0, 2, 3, 2, 0]]


def get_resize_factor(size_x, size_y):
    size_factor = size_x if size_x > size_y else size_y
    resize_factor = 1
    if size_factor > 128:
        resize_factor = (size_factor - 128) / 128 + 1
    return resize_factor


def get_char(brightness, error):
    brightness = brightness + error
    coefficient = 255 / (len(COLORS_TABLE) - 1)
    char = COLORS_TABLE[int(brightness / coefficient)]
    return char, brightness - (COLORS_TABLE.index(char) * coefficient)


def get_color(r, g, b):
    ir = 255 if r >= 128 else 0
    ig = 255 if g >= 128 else 0
    ib = 255 if b >= 128 else 0
    return (ir, ig, ib), [r - ir, g - ig, b - ib].copy()


def check_pos(x, y, ix, iy):
    if ix < 0 or iy < 0 or ix >= x or iy >= y:
        return False
    return True


def image_to_ascii_art(image_path, blending_mode, coloring_mode):
    img = Image.open(image_path)

    extension = image_path[image_path.rfind(".") + 1::]

    data = [[]]
    if extension not in {"gif"}:
        print("Working with image...")
        resize_factor = get_resize_factor(img.size[0], img.size[1])

        img = img.reduce(int(resize_factor))
        pixels = img.load()
        x, y = img.size
        data[0] = (x, y)

        data.append([])

        for iy in range(y):
            error = 0
            for ix in range(x):
                pixel = pixels[ix, iy]
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                brightness = r * 0.3 + g * 0.59 + b * 0.11
                char, error = get_char(brightness, error)
                if coloring_mode:
                    color, color_error = get_color(r, g, b)
                    if blending_mode:
                        for dy in range(3):
                            for dx in range(-2, 3):
                                if dy == 0 and dx <= 0:
                                    continue
                                if check_pos(x, y, ix + dx, iy + dy):
                                    p = pixels[ix + dx, iy + dy]
                                    pixels[ix + dx, iy + dy] = (
                                        p[0] + int(BLEND_MAP[dy][dx + 2] * color_error[0] / 32),
                                        p[1] + int(BLEND_MAP[dy][dx + 2] * color_error[1] / 32),
                                        p[2] + int(BLEND_MAP[dy][dx + 2] * color_error[2] / 32))
                else:
                    color = (255, 255, 255)

                data[1].append((char, color, [ix, iy]))

    # HnTR - Working with gifs
    else:
        data = [[]]
        frame_id = 0
        for frame in [frame.copy() for frame in ImageSequence.Iterator(img)]:
            if frame.mode == "P":
                continue

            print(f"Working with frame {frame_id}...")

            resize_factor = get_resize_factor(frame.size[0], frame.size[1])
            frame = frame.reduce(int(resize_factor))
            pixels = frame.load()
            x, y = frame.size
            data[0] = (x, y)

            data.append([])

            for iy in range(y):
                error = 0
                for ix in range(x):
                    pixel = pixels[ix, iy]
                    r = pixel[0]
                    g = pixel[1]
                    b = pixel[2]
                    brightness = r * 0.3 + g * 0.59 + b * 0.11
                    char, error = get_char(brightness, error)
                    if coloring_mode:
                        color, color_error = get_color(r, g, b)
                        if blending_mode:
                            for dy in range(3):
                                for dx in range(-2, 3):
                                    if dy == 0 and dx <= 0:
                                        continue
                                    if check_pos(x, y, ix + dx, iy + dy):
                                        p = pixels[ix + dx, iy + dy]
                                        pixels[ix + dx, iy + dy] = (
                                            p[0] + int(BLEND_MAP[dy][dx + 2] * color_error[0] / 32),
                                            p[1] + int(BLEND_MAP[dy][dx + 2] * color_error[1] / 32),
                                            p[2] + int(BLEND_MAP[dy][dx + 2] * color_error[2] / 32))
                    else:
                        color = (255, 255, 255)

                    data[-1].append((char, color, [ix, iy]))

            frame_id += 1

    img.close()
    return data
