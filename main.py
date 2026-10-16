import pygame
from settings import *
from objects.solar_system import objects
from physics.gravity import update
from graphics.renderer import draw
from graphics.camera import Camera
from ui.interface import draw_hud
from collections import deque
from physics.energy import total_energy
from ui.interface import draw_hud, draw_energy_graph

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
camera = Camera()

dragging = False
last_mouse_pos = None

pygame.display.set_caption("Солнечная система")

# Локальные настройки физики (можно менять клавишами)
physics_steps = PHYSICS_STEPS
dt = 600

# Границы, чтобы случайно не уйти в ноль или в бесконечность
DT_MIN = 1
DT_MAX = 86400  # 1 сутки
STEPS_MIN = 1
STEPS_MAX = 1000
model_time = 0.0
energy_history = deque(maxlen=1_000_000)
focus_idx = None  # None = свободная камера

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
                last_mouse_pos = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # ПКМ
                dragging = False
                last_mouse_pos = None

        if event.type == pygame.KEYDOWN:
            # Скорость симуляции: PHYSICS_STEPS
            if event.key in (pygame.K_EQUALS, pygame.K_PLUS, pygame.K_KP_PLUS):
                physics_steps = min(STEPS_MAX, physics_steps + 10)
            if event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                physics_steps = max(STEPS_MIN, physics_steps - 10)

            # Точность симуляции: dt (в 2 раза)
            if event.key in (pygame.K_PERIOD, pygame.K_KP_PERIOD):
                dt = min(DT_MAX, dt * 2)
            if event.key == pygame.K_COMMA:
                dt = max(DT_MIN, dt // 2)

            if event.key == pygame.K_TAB:
                if focus_idx is None:
                    focus_idx = 0
                elif focus_idx >= len(objects) - 1:
                    focus_idx = None
                else:
                    focus_idx += 1

        if event.type == pygame.MOUSEWHEEL:
            mx, my = pygame.mouse.get_pos()
            # мировая точка под курсором до зума
            wx = (mx - WIDTH / 2 + camera.x * camera.scale)
            wy = (my - HEIGHT / 2 + camera.y * camera.scale)
            factor = 1.1 if event.y > 0 else 1 / 1.1
            camera.scale /= factor
            # сдвигаем камеру, чтобы точка осталась под курсором
            camera.x = wx / camera.scale - (mx - WIDTH / 2) / camera.scale
            camera.y = wy / camera.scale - (my - HEIGHT / 2) / camera.scale

    if dragging:
        mouse_pos = pygame.mouse.get_pos()

        dx = mouse_pos[0] - last_mouse_pos[0]
        dy = mouse_pos[1] - last_mouse_pos[1]

        camera.drag(dx, dy)

        last_mouse_pos = mouse_pos

    if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
        focus_idx = None

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

    update(objects, dt, physics_steps)
    if focus_idx is not None:
        target = objects[focus_idx]
        camera.x = target.x / camera.scale
        camera.y = target.y / camera.scale
    model_time += dt * physics_steps
    energy_history.append(total_energy(objects, G))
    draw(screen, objects, camera)
    days = model_time / 86400
    if days < 365:
        time_str = f"{days:.1f} сут"
    else:
        time_str = f"{days / 365.25:.2f} лет"
    draw_hud(screen, dt, physics_steps, extra_lines=[
        f"время       = " + time_str,
    ])
    draw_energy_graph(screen, energy_history)
    pygame.display.flip()

pygame.quit()
