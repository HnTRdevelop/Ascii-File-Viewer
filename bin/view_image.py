import pygame
import sys


def display_image(image_data):
    font_size = 8

    pygame.init()
    pygame.font.init()

    font = pygame.font.Font('font.ttf', font_size)
    font_size -= 1

    size = image_data.pop(0)
    screen = pygame.display.set_mode((size[0] * font_size, size[1] * font_size))

    frame_id = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        if frame_id >= len(image_data):
            frame_id = 0

        frame = image_data[frame_id]
        for pixel in frame:
            char = pixel[0]

            color = pixel[1]
            pos = pixel[2]
            char_draw = font.render(char, False, color)
            screen.blit(char_draw, (pos[0] * font_size, pos[1] * font_size))

        frame_id += 1
        clock.tick(24)
        pygame.display.flip()
