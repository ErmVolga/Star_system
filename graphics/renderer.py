from settings import BACKGROUND_COLOR
import pygame


def draw(screen, objects, camera):
    screen.fill(BACKGROUND_COLOR)

    for object1 in objects:
        screen_pos = camera.world_to_screen(
            (object1.x, object1.y)
        )

        pygame.draw.circle(screen, object1.color, (round(screen_pos[0]), round(screen_pos[1])), object1.radius)
