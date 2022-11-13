import pygame
from pygame import mixer


pygame.init()

screen = pygame.display.set_mode((800, 600))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((0, 0, 0))

    pygame.display.flip()
