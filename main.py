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

pygame.display.set_caption("Солнечная система")

# 1 реальная секунда = dt * тик * PHYSICS_STEPS (с)
dt = 3600

running = True
while running:

    clock.tick(60)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if keys[pygame.K_a]:
        if keys[pygame.K_LSHIFT]:
            camera.move(-camera.speed / 30, 0)
        camera.move(-camera.speed / 60, 0)

    if keys[pygame.K_d]:
        if keys[pygame.K_LSHIFT]:
            camera.move(camera.speed / 30, 0)
        camera.move(camera.speed / 60, 0)

    if keys[pygame.K_w]:
        if keys[pygame.K_LSHIFT]:
            camera.move(0, -camera.speed / 30)
        camera.move(0, -camera.speed / 60)

    if keys[pygame.K_s]:
        if keys[pygame.K_LSHIFT]:
            camera.move(0, camera.speed / 30)
        camera.move(0, camera.speed / 60)

    update(objects, dt)
    draw(screen, objects, camera)
    pygame.display.flip()

pygame.quit()
