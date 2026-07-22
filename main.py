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

dragging = False
last_mouse_pos = None

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

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # ПКМ
                dragging = True
                last_mouse_pos = event.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # ПКМ
                dragging = False
                last_mouse_pos = None

        if dragging:
            mouse_pos = pygame.mouse.get_pos()

            dx = mouse_pos[0] - last_mouse_pos[0]
            dy = mouse_pos[1] - last_mouse_pos[1]

            camera.drag(dx, dy)

            last_mouse_pos = mouse_pos

    if keys[pygame.K_a]:
        speed = camera.keyboard_speed / 60
        if keys[pygame.K_LSHIFT]:
            speed *= 3
        camera.move(-speed, 0)

    if keys[pygame.K_d]:
        speed = camera.keyboard_speed / 60
        if keys[pygame.K_LSHIFT]:
            speed *= 3
        camera.move(speed, 0)

    if keys[pygame.K_w]:
        speed = camera.keyboard_speed / 60
        if keys[pygame.K_LSHIFT]:
            speed *= 3
        camera.move(0, -speed)

    if keys[pygame.K_s]:
        speed = camera.keyboard_speed / 60
        if keys[pygame.K_LSHIFT]:
            speed *= 3
        camera.move(0, speed)

    update(objects, dt)
    draw(screen, objects, camera)
    pygame.display.flip()

pygame.quit()
