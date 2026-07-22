import pygame
from settings import *
from objects.solar_system import objects
from physics.gravity import update
from graphics.renderer import draw

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Солнечная система")

# 1 реальная секунда = dt * тик * PHYSICS_STEPS (с)
dt = 3600

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    update(objects, dt)
    draw(screen, objects)
    pygame.display.flip()

pygame.quit()
