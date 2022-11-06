import pygame
import sys


def quit_viewer():
    pygame.quit()
    sys.exit()


def display_image(image_data, image_name):
    font_size = 16

    pygame.init()
    pygame.font.init()

    font = pygame.font.Font('font.ttf', font_size)
    font_size -= 1

    img_data = image_data.pop(0)
    size = img_data[:2]
    frame_rate = img_data[2]

    frames = []
    for frame_data in image_data:
        frame_surface = pygame.Surface((size[0] * font_size, size[1] * font_size))
        for pixel in frame_data:
            char = pixel[0]
            color = pixel[1]
            pos = pixel[2]
            char_draw = font.render(char, True, color)
            frame_surface.blit(char_draw, (pos[0] * font_size, pos[1] * font_size))
        frames.append(frame_surface)

    frame_size = frames[0].get_size()
    screen_size = (1920, 1080)

    resize_factor = frame_size[0] / screen_size[0] \
        if frame_size[1] / screen_size[1] < frame_size[0] / screen_size[0] \
        else frame_size[1] / screen_size[1]

    screen = pygame.display.set_mode((frame_size[0] / resize_factor, frame_size[1] / resize_factor))
    pygame.display.set_caption(image_name)

    clock = pygame.time.Clock()
    frame_id = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_viewer()

        if frame_id >= len(frames):
            frame_id = 0
        frame = frames[frame_id]
        frame_id += 1

        screen.fill((0, 0, 0))

        frame_surface = pygame.transform.smoothscale(frame, screen.get_size())
        screen.blit(frame_surface, (0, 0))

        clock.tick(int(frame_rate))
        pygame.display.flip()
