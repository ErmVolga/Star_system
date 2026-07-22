from settings import BACKGROUND_COLOR, CENTER_X, CENTER_Y, SCALE
from objects.solar_system import Sun
import pygame

pygame.init()


def draw(screen, objects):
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, Sun.color, (CENTER_X, CENTER_Y), Sun.radius)

    for object1 in objects[1:]:
        object1_screen_x = CENTER_X + object1.x / SCALE
        object1_screen_y = CENTER_Y + object1.y / SCALE
        pygame.draw.circle(screen, object1.color, (round(object1_screen_x), round(object1_screen_y)), object1.radius)

    pygame.display.flip()
