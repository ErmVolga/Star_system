from settings import BACKGROUND_COLOR, CENTER_X, CENTER_Y, SCALE
import pygame


def draw(screen, objects, camera):
    screen.fill(BACKGROUND_COLOR)

    for object1 in objects:
        object1_screen_x = CENTER_X + object1.x / SCALE
        object1_screen_y = CENTER_Y + object1.y / SCALE
        world_pos = (
            object1.x / SCALE,
            object1.y / SCALE
        )

        screen_pos = camera.world_to_screen(world_pos)

        pygame.draw.circle(screen, object1.color, (round(screen_pos[0]), round(screen_pos[1])), object1.radius)
