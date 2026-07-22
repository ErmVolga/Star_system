from settings import BACKGROUND_COLOR, CENTER_X, CENTER_Y, SCALE
import pygame


def draw(screen, objects):
    screen.fill(BACKGROUND_COLOR)

    for object1 in objects:
        object1_screen_x = CENTER_X + object1.x / SCALE
        object1_screen_y = CENTER_Y + object1.y / SCALE
        pygame.draw.circle(screen, object1.color, (round(object1_screen_x), round(object1_screen_y)), object1.radius)
