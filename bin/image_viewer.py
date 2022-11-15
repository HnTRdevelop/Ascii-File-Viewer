import pygame

FONT_SIZE = 16


def display_image(image_data, image_name):
    # Запускаем нужные библиотеки pygame
    pygame.init()
    pygame.font.init()

    # Загружаем шрифт
    font = pygame.font.Font('font.ttf', FONT_SIZE)

    # Удаляем расширение файла у имени
    image_name = image_name[:image_name.rfind("."):]

    # Читаем информацию об файле
    img_data = image_data.pop(0)
    size = img_data[:2]
    frame_rate = img_data[2]

    # Создаём список кадров
    frames = []
    for frame_data in image_data:

        # Создаём кадр
        frame_surface = pygame.Surface((size[0] * FONT_SIZE, size[1] * FONT_SIZE))

        # Читаем информацию об символах и рисуем их
        for pixel in frame_data:
            char = pixel[0]
            color = pixel[1]
            pos = pixel[2]
            char_draw = font.render(char, True, color)
            frame_surface.blit(char_draw, (pos[0] * FONT_SIZE, pos[1] * FONT_SIZE))

        # Сохраняем кадр в список
        frames.append(frame_surface)

    # Высчитываем размеры окна в зависимости от размеров картинки и размеров экрана
    frame_size = frames[0].get_size()
    # screen_info = get_monitors(Enumerator.Windows)
    screen_size = (1920 / 1.5, 1080 / 1.5)

    resize_factor = frame_size[0] / screen_size[0] \
        if frame_size[1] / screen_size[1] < frame_size[0] / screen_size[0] \
        else frame_size[1] / screen_size[1]

    # Создаём окно pygame
    screen = pygame.display.set_mode((frame_size[0] / resize_factor, frame_size[1] / resize_factor))
    pygame.display.set_caption(image_name)

    # Создаём clock
    clock = pygame.time.Clock()
    frame_id = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Сохраняем изображение при выходе
                pygame.image.save(frames[0], f"outputs/{image_name}.png")
                pygame.quit()
                running = False

        if running:
            # Обнуляем счётчик кадра если мы уходим за границы списка кадров
            if frame_id >= len(frames):
                frame_id = 0

            # Считываем кадр по счётчику
            frame = frames[frame_id]

            # Увеличиваем счётчик кадров на один
            frame_id += 1

            # Заполняем экран чёрным цветом
            screen.fill((0, 0, 0))

            # Подгоняем размер кадра под экран
            frame_surface = pygame.transform.smoothscale(frame, screen.get_size())

            # Рисуем кадр
            screen.blit(frame_surface, (0, 0))

            # Обновляем окно pygame с fps равный fps у файла
            clock.tick(int(frame_rate))
            pygame.display.flip()
