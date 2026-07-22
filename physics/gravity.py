from settings import PHYSICS_STEPS, G
from math import sqrt

def universal_gravity(G, m1, m2, r):
    return G * m1 * m2 / r ** 2

def update(objects, dt):
    for step in range(PHYSICS_STEPS):
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