from PIL import Image, ImageSequence


COLORS_TABLE = " .:-=+*#%@"
BLEND_MAP = [[0, 0, 0, 5, 3],
             [2, 4, 5, 4, 2],
             [0, 2, 3, 2, 0]]
BLEND_DIVIDER = 32


# Функция для расчёта фактора уменьшении изображения
def get_resize_factor(size_x, size_y):
    size_factor = size_x if size_x > size_y else size_y
    resize_factor = 1
    if size_factor > 128:
        resize_factor = (size_factor - 128) / 128 + 1
    return resize_factor


# Функция для получения символа в зависимости от яркости пикселя
def get_char(brightness, error):
    brightness = brightness + error
    coefficient = 255 / (len(COLORS_TABLE) - 1)
    char = COLORS_TABLE[int(brightness / coefficient)]
    return char, brightness - (COLORS_TABLE.index(char) * coefficient)


# Функция для расчёта цвета пикселя
def get_color(r, g, b):
    ir = 255 if r >= 128 else 0
    ig = 255 if g >= 128 else 0
    ib = 255 if b >= 128 else 0
    return (ir, ig, ib), [r - ir, g - ig, b - ib]


# Формула для проверки существования пикселя
def check_pos(x, y, ix, iy):
    if ix < 0 or iy < 0 or ix >= x or iy >= y:
        return False
    return True


# Функия для обработки пикселя
def compute_pixel(pixel, error):
    # Читаем цвет пикселя
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    # Расчитываем яркость пикселя
    brightness = r * 0.3 + g * 0.59 + b * 0.11

    # Получаем символ и ошибку яркости
    char, error = get_char(brightness, error)

    # Получаем цвет и ошибку цвета
    color, color_error = get_color(r, g, b)

    return char, color, error, color_error



def image_to_ascii_art(image_path, blending_mode, coloring_mode):
    # Открываем файл
    img = Image.open(image_path)

    # Узнаём расширение
    extension = image_path[image_path.rfind(".")::]

    # Создаём список для хранения данных об фале
    data = [[]]

    # Работа с изображениями если расширение не .gif
    if extension != ".gif":
        # Получаем фактор уменьшения картинки
        resize_factor = get_resize_factor(img.size[0], img.size[1])

        # Уменьшаем картинку
        img = img.reduce(int(resize_factor))

        # Читаем информацию об картинке
        pixels = img.load()
        x, y = img.size

        # Сохраняем размер картинки в список данных об картинке
        data[0] = (x, y, 0)

        # Добавляем пустой список в список данных для сохранения туда пикселей
        data.append([])

        # Обрабатываем пиксели
        for iy in range(y):
            # Создаём переменную для хранения ошибки яркости
            error = 0

            for ix in range(x):
                # Получаем пиксель по координатам
                pixel = pixels[ix, iy]

                # Получаем готовые даннные об пикселе
                char, color, error, color_error = compute_pixel(pixel, error)

                # Если режим передачи цвета выключен, то рисуем пиксель белым
                if not coloring_mode:
                    color = (255, 255, 255)

                # Если включён режим смешения цветов, то распространяем ошибку на соседние пиксели
                if blending_mode:
                    for dy in range(3):
                        for dx in range(-2, 3):
                            if dy == 0 and dx <= 0:
                                continue
                            if check_pos(x, y, ix + dx, iy + dy):
                                p = pixels[ix + dx, iy + dy]
                                pixels[ix + dx, iy + dy] = (
                                    p[0] + int(BLEND_MAP[dy][dx + 2] * color_error[0] / BLEND_DIVIDER),
                                    p[1] + int(BLEND_MAP[dy][dx + 2] * color_error[1] / BLEND_DIVIDER),
                                    p[2] + int(BLEND_MAP[dy][dx + 2] * color_error[2] / BLEND_DIVIDER))

                # Добавляем данные об пикселе в список
                data[-1].append((char, color, [ix, iy]))

    # Работа с .gif форматом
    else:
        # Пропускаем кард, если его режим "P"
        for frame in [frame.copy() for frame in ImageSequence.Iterator(img)]:
            if frame.mode == "P":
                continue

            # Получаем фактор уменьшения кадра
            resize_factor = get_resize_factor(frame.size[0], frame.size[1])

            # Уменьшаем кадр
            frame = frame.reduce(int(resize_factor))

            # Читаем информацию об кадре
            pixels = frame.load()
            x, y = frame.size
            data[0] = (x, y, 1000 / img.info["duration"])

            # Добавляем пустой кадр в список данных для сохранения туда пикселей
            data.append([])

            for iy in range(y):
                error = 0
                for ix in range(x):
                    # Получаем пиксель по координатам
                    pixel = pixels[ix, iy]

                    # Получаем готовые даннные об пикселе
                    char, color, error, color_error = compute_pixel(pixel, error)

                    # Если режим передачи цвета выключен, то рисуем пиксель белым
                    if not coloring_mode:
                        color = (255, 255, 255)

                    # Если включён режим смешения цветов, то распространяем ошибку на соседние пиксели
                    if blending_mode:
                        for dy in range(3):
                            for dx in range(-2, 3):
                                if dy == 0 and dx <= 0:
                                    continue
                                if check_pos(x, y, ix + dx, iy + dy):
                                    p = pixels[ix + dx, iy + dy]
                                    pixels[ix + dx, iy + dy] = (
                                        p[0] + int(BLEND_MAP[dy][dx + 2] * color_error[0] / BLEND_DIVIDER),
                                        p[1] + int(BLEND_MAP[dy][dx + 2] * color_error[1] / BLEND_DIVIDER),
                                        p[2] + int(BLEND_MAP[dy][dx + 2] * color_error[2] / BLEND_DIVIDER))

                    # Добавляем пиксель в последний кадр
                    data[-1].append((char, color, [ix, iy]))

    # Закрываем файл
    img.close()

    # Возвращаем данные о файле
    return data
