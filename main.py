import pygame
from math import sqrt
from settings import *

pygame.init()


class SpaceObject:
    def __init__(self, name, x, y, vx, vy, color, radius, mass, fixed=False):
        self.name = name

        # Физические координаты (метры)
        self.x = x
        self.y = y

        # Скорость (м/с)
        self.vx = vx
        self.vy = vy

        # Ускорение (м/с²)
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


# -------------------------------------------------
# Масштаб
# -------------------------------------------------

# 1 а.е. = 400 пикселей
SCALE = AU / 400

CENTER_X = WIDTH // 2
CENTER_Y = HEIGHT // 2

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

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Солнечная система")

# Один кадр = 12 часов
dt = 86400

running = True
while running:

    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for object1 in objects[1:]:
        object1.ax = 0
        object1.ay = 0
        for object2 in objects:
            dx = object2.x - object1.x
            dy = object2.y - object1.y

            R = sqrt(dx ** 2 + dy ** 2)
            if R == 0:
                continue

            F = universal_gravity(G, object2.mass, object1.mass, R)

            # Единичный вектор
            ux = dx / R
            uy = dy / R

            # Проекции силы
            Fx = F * ux
            Fy = F * uy

            object1.ax += Fx / object1.mass
            object1.ay += Fy / object1.mass

    for object1 in objects[1:]:
        object1.update(dt)

    # ---------------------------------------------
    # ОТРИСОВКА
    # ---------------------------------------------

    screen.fill(BACKGROUND_COLOR)

    pygame.draw.circle(screen, Sun.color, (CENTER_X, CENTER_Y), Sun.radius)
    for object1 in objects[1:]:
        if len(object1.path) > 1:
            points = []

            for x, y in object1.path:
                px = CENTER_X + x / SCALE
                py = CENTER_Y + y / SCALE
                points.append((round(px), round(py)))

            pygame.draw.lines(screen, object1.color, False, points, 1)


    for object1 in objects[1:]:
        object1_screen_x = CENTER_X + object1.x / SCALE
        object1_screen_y = CENTER_Y + object1.y / SCALE
        pygame.draw.circle(screen, object1.color, (round(object1_screen_x), round(object1_screen_y)), object1.radius)

    pygame.display.flip()

pygame.quit()
