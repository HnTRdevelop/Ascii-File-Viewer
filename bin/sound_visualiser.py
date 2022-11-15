from pydub import AudioSegment
import pygame


FONT_SIZE = 32


# Функция для расчёта цвета
def rainbow_color(value):
    step = (value // 256) % 6
    pos = value % 256

    if step == 0:
        return (255, pos, 0)
    if step == 1:
        return (255 - pos, 255, 0)
    if step == 2:
        return (0, 255, pos)
    if step == 3:
        return (0, 255 - pos, 255)
    if step == 4:
        return (pos, 0, 255)
    if step == 5:
        return (255, 0, 255 - pos)


def visualise_sound(file_path, file_name):
    # Запускаем нужные библиотеки pygame
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()

    # Загружаем звуковой файл
    sound = AudioSegment.from_file(file_path)
    pygame_sound = pygame.mixer.Sound(file_path)

    # Загружаем шрифт
    font = pygame.font.Font('font.ttf', FONT_SIZE)
    file_name = file_name[:file_name.rfind("."):]

    # Читаем информацию об экране
    # screen_info = get_monitors()[0]
    screen_size = (1920 / 2, 1080 / 2)

    # Создаём окно pygame
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(file_name)

    # Создаём clock
    clock = pygame.time.Clock()
    color_value = 0

    # Создаём список линий визуалайзера
    lines = [0 for _ in range(int(screen_size[0] / FONT_SIZE))]
    pygame_sound.set_volume(0.2)
    pygame_sound.play()

    # Создаём переменные для обработки линий
    gravity = 14 * screen_size[1] / 16 * 2
    t = 0
    last_t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        # Закрываем pygame если музыка закончилась
        if t > sound.duration_seconds:
            pygame.quit()
            running = False

        if running:
            # Высчитываем время между кадрами (в ms)
            delta_time = clock.get_time() / 1000
            t += delta_time

            # Заполняем экран чёрным цветом
            screen.fill((0, 0, 0))

            # Высчитываем амплитуду в момент времени между кадрами
            frequency = sound[last_t * 1000:t * 1000].max
            amplitude = frequency / sound.max

            # Узнаём индекс линии для обработки
            line_id = int(amplitude * len(lines))

            # Это не удалять, без этого куска ошибка
            if line_id > len(lines) - 1:
                line_id = len(lines) - 1
            if line_id < 0:
                line_id = 0
            # Это не удалять, без этого куска ошибка

            # Выставляем высоту для нужной линии
            lines[line_id] = screen_size[1] / 2

            # Высчитываем следующий цвет
            color_value = (color_value + 1) % (256 * 6)

            # Рисуем линии
            for line in range(len(lines)):
                # Задаём минимум для значении линии
                if lines[line] < FONT_SIZE:
                    lines[line] = FONT_SIZE

                # Высчитываем высоту линии
                line_height = lines[line]

                # Опускаем значение линии на определённую константу
                lines[line] -= gravity * delta_time

                # Рисуем символы в зависимости от высоты линии
                for i in range(int(line_height // FONT_SIZE)):
                    char_draw = font.render("()", True,
                                            rainbow_color(color_value))
                    screen.blit(char_draw, (line * FONT_SIZE,
                                            screen_size[1] / 2 - i * FONT_SIZE))
                    screen.blit(char_draw, (line * FONT_SIZE,
                                            screen_size[1] / 2 + i * FONT_SIZE))

            # Сохраняем время последнего кадра
            last_t = t

            # Обновляем экран без ограничения fps
            clock.tick(0)
            pygame.display.flip()
