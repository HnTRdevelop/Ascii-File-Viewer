from pydub import AudioSegment
import pygame
import itertools


FONT_SIZE = 32


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
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.mixer.init()
    pygame.init()
    pygame.font.init()

    sound = AudioSegment.from_file(file_path)
    pygame_sound = pygame.mixer.Sound(file_path)

    font = pygame.font.Font('font.ttf', FONT_SIZE)

    pygame.display.set_mode((0, 0))
    screen_info = pygame.display.Info()
    screen_size = (screen_info.current_w / 2, screen_info.current_h / 2)

    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(file_name)

    clock = pygame.time.Clock()
    color_value = 0

    lines = [0 for _ in range(int(screen_size[0] / FONT_SIZE))]
    pygame_sound.set_volume(0.2)
    pygame_sound.play()

    gravity = 14 * screen_size[1] / 16 * 2
    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

        if t > sound.duration_seconds:
            pygame.quit()
            running = False

        if running:
            delta_time = clock.get_time() / 1000
            t += delta_time

            screen.fill((0, 0, 0))

            frequency = sound[t * 1000].max
            amplitude = frequency / sound.max
            line_id = int(amplitude * len(lines))
            if line_id > len(lines) - 1:
                line_id = len(lines) - 1
            if line_id < 0:
                line_id = 0
            lines[line_id] = screen_size[1] / 2

            color_value = (color_value + 1) % (256 * 6)
            for line in range(len(lines)):
                if lines[line] < FONT_SIZE:
                    lines[line] = FONT_SIZE
                line_height = lines[line]
                lines[line] -= gravity * delta_time

                for i in range(int(line_height // FONT_SIZE)):
                    char_draw = font.render("()", True,
                                            rainbow_color(color_value))
                    screen.blit(char_draw, (line * FONT_SIZE,
                                            screen_size[1] / 2 - i * FONT_SIZE))
                    screen.blit(char_draw, (line * FONT_SIZE,
                                            screen_size[1] / 2 + i * FONT_SIZE))
            clock.tick(0)
            pygame.display.flip()
