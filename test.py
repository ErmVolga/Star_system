import pygame
from math import sqrt
from settings import *

pygame.init()

# ---------- Шрифт для текста ----------
font = pygame.font.SysFont('Arial', 24)

class SpaceObject:
    def __init__(self, name, x, y, vx, vy, color, radius, mass, fixed=False):
        self.name = name
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.color = color
        self.radius = radius
        self.mass = mass
        self.fixed = fixed
        self.path = []

    def update(self, dt):
        if self.fixed:
            return
        self.vx += self.ax * dt
        self.vy += self.ay * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.path.append((self.x, self.y))
        if len(self.path) > 1200:
            self.path.pop(0)

    def __str__(self):
        return f"{self.name}: x={self.x:.2f}, y={self.y:.2f}"

def universal_gravity(G, m1, m2, r):
    return G * m1 * m2 / r ** 2

# ---------- Функция полной механической энергии ----------
def total_energy(objects):
    K = 0.0
    U = 0.0
    # Кинетическая энергия всех тел
    for obj in objects:
        v2 = obj.vx**2 + obj.vy**2
        K += 0.5 * obj.mass * v2
    # Потенциальная энергия для каждой пары (i < j)
    for i in range(len(objects)):
        for j in range(i+1, len(objects)):
            obj1 = objects[i]
            obj2 = objects[j]
            dx = obj2.x - obj1.x
            dy = obj2.y - obj1.y
            r = sqrt(dx*dx + dy*dy)
            if r == 0:
                continue
            U -= G * obj1.mass * obj2.mass / r
    return K + U

# -------------------------------------------------
# Масштаб и камера
# -------------------------------------------------
SCALE = AU / 400
CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

# Переменные камеры (смещение в пикселях)
camera_x = 0.0
camera_y = 0.0
dragging = False

# -------------------------------------------------
# Создание объектов
# -------------------------------------------------
Sun = SpaceObject("Солнце", 0, 0, 0, 0, YELLOW, 30, 332940 * EARTH_MASS, True)
Mercury = SpaceObject("Меркурий", 0.466697 * AU, 0, 0, -38860, GREY, 10, 0.055274 * EARTH_MASS)
Venus = SpaceObject("Венера", 0.728213 * AU, 0, 0, -34790, BEGEVY, 10, 0.815 * EARTH_MASS)
Earth = SpaceObject("Земля", 1.0167086 * AU, 0, 0, -29290, BLUE, 10, EARTH_MASS)
Moon = SpaceObject("Луна", Earth.x + 405400000, 0, 0, Earth.vy + 964, WHITE, 2, EARTH_MASS / 81.3)
Mars = SpaceObject("Марс", 1.66621 * AU, 0, 0, -21970, RED, 10, 0.107 * EARTH_MASS)
objects = [Sun, Earth, Moon, Mercury, Venus, Mars]

# ---------- Начальная энергия ----------
initial_energy = total_energy(objects)
print(f"Начальная энергия: {initial_energy:.6e} Дж")

# Переменные для вывода
frame_count = 0
current_energy = initial_energy
percent_change = 0.0

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Солнечная система")

dt = 86400   # 12 часов за кадр
running = True

while running:
    clock.tick(30)

    # ---------- Обработка событий ----------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # ПКМ для перемещения камеры
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            dragging = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            dragging = False
        if event.type == pygame.MOUSEMOTION and dragging:
            dx, dy = event.rel
            camera_x += dx
            camera_y += dy

    # ---------- Физика (только для планет, не для Солнца) ----------
    for object1 in objects[1:]:  # все кроме Солнца
        object1.ax = 0
        object1.ay = 0
        for object2 in objects:  # учитываем влияние всех тел (включая Солнце)
            dx = object2.x - object1.x
            dy = object2.y - object1.y
            R = sqrt(dx ** 2 + dy ** 2)
            if R == 0:
                continue
            F = universal_gravity(G, object2.mass, object1.mass, R)
            ux = dx / R
            uy = dy / R
            Fx = F * ux
            Fy = F * uy
            object1.ax += Fx / object1.mass
            object1.ay += Fy / object1.mass

    for object1 in objects[1:]:
        object1.update(dt)

    # ---------- Подсчёт энергии каждые 60 кадров ----------
    frame_count += 1
    if frame_count % 60 == 0:
        current_energy = total_energy(objects)
        percent_change = ((current_energy - initial_energy) / abs(initial_energy)) * 100
        print(f"Кадр {frame_count}: энергия = {current_energy:.6e} Дж, изменение = {percent_change:.6f}%")

    # ---------- Отрисовка ----------
    screen.fill(BACKGROUND_COLOR)

    # Солнце (фиксированное, без траектории)
    sun_screen_x = CENTER_X + Sun.x / SCALE + camera_x
    sun_screen_y = CENTER_Y + Sun.y / SCALE + camera_y
    pygame.draw.circle(screen, Sun.color, (round(sun_screen_x), round(sun_screen_y)), Sun.radius)

    # Планеты (траектории и сами объекты)
    for object1 in objects[1:]:
        # Траектория
        if len(object1.path) > 1:
            points = []
            for x, y in object1.path:
                px = CENTER_X + x / SCALE + camera_x
                py = CENTER_Y + y / SCALE + camera_y
                points.append((round(px), round(py)))
            pygame.draw.lines(screen, object1.color, False, points, 1)

        # Сам объект
        obj_screen_x = CENTER_X + object1.x / SCALE + camera_x
        obj_screen_y = CENTER_Y + object1.y / SCALE + camera_y
        pygame.draw.circle(screen, object1.color, (round(obj_screen_x), round(obj_screen_y)), object1.radius)

    # ---------- Вывод информации на экран ----------
    text1 = font.render(f"Энергия: {current_energy:.3e} Дж", True, WHITE)
    text2 = font.render(f"Изменение: {percent_change:.4f}%", True, WHITE)
    text3 = font.render(f"Начальная: {initial_energy:.3e} Дж", True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    screen.blit(text3, (10, 70))

    pygame.display.flip()

pygame.quit()