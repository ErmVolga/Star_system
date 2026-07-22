import pygame
from settings import *
from objects.solar_system import objects
from physics.gravity import update
from graphics.renderer import draw
from graphics.camera import Camera

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
camera = Camera()
keys = pygame.key.get_pressed()


pygame.display.set_caption("Солнечная система")

# 1 реальная секунда = dt * тик * PHYSICS_STEPS (с)
dt = 3600

running = True
while running:

    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if keys[pygame.K_a]:
            camera.x -= speed

        if keys[pygame.K_d]:
            camera.x += speed

        if keys[pygame.K_w]:
            camera.y -= speed

        if keys[pygame.K_s]:
            camera.y += speed

    update(objects, dt)
    draw(screen, objects, camera)
    pygame.display.flip()

pygame.quit()
