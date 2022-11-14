import pygame


FONT_SIZE = 16


def quit_viewer():
    pygame.quit()


def display_image(image_data, image_name):
    pygame.init()
    pygame.font.init()

    font = pygame.font.Font('font.ttf', FONT_SIZE)

    img_data = image_data.pop(0)
    size = img_data[:2]
    frame_rate = img_data[2]

    frames = []
    for frame_data in image_data:
        frame_surface = pygame.Surface((size[0] * FONT_SIZE, size[1] * FONT_SIZE))
        for pixel in frame_data:
            char = pixel[0]
            color = pixel[1]
            pos = pixel[2]
            char_draw = font.render(char, True, color)
            frame_surface.blit(char_draw, (pos[0] * FONT_SIZE, pos[1] * FONT_SIZE))
        frames.append(frame_surface)

    frame_size = frames[0].get_size()
    pygame.display.set_mode((0, 0))
    screen_info = pygame.display.Info()
    screen_size = (screen_info.current_w / 1.5, screen_info.current_h / 1.5)

    resize_factor = frame_size[0] / screen_size[0] \
        if frame_size[1] / screen_size[1] < frame_size[0] / screen_size[0] \
        else frame_size[1] / screen_size[1]

    screen = pygame.display.set_mode((frame_size[0] / resize_factor, frame_size[1] / resize_factor))
    pygame.display.set_caption(image_name)

    clock = pygame.time.Clock()
    frame_id = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.image.save(frames[0], f"outputs/{image_name}.png")
                quit_viewer()
                running = False

        if running:
            if frame_id >= len(frames):
                frame_id = 0
            frame = frames[frame_id]
            frame_id += 1

            screen.fill((0, 0, 0))

            frame_surface = pygame.transform.smoothscale(frame, screen.get_size())
            screen.blit(frame_surface, (0, 0))

            clock.tick(int(frame_rate))
            pygame.display.flip()
