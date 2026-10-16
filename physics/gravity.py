import settings
from math import sqrt


def compute_accelerations(objects):
    """
    Вычисляет ускорения для всех объектов (кроме fixed) на основе текущих позиций.
    Результат записывается в поля ax, ay каждого объекта.
    """
    # Обнуляем ускорения для подвижных объектов
    for obj in objects:
        if not obj.fixed:
            obj.ax = 0.0
            obj.ay = 0.0

    # Для каждой пары объектов вычисляем силу
    for i, obj1 in enumerate(objects):
        if obj1.fixed:
            continue
        for j, obj2 in enumerate(objects):
            if i == j:
                continue
            dx = obj2.x - obj1.x
            dy = obj2.y - obj1.y
            r2 = dx * dx + dy * dy
            if r2 == 0:
                continue
            r = sqrt(r2)
            # Сила со стороны obj2 на obj1
            F = settings.G * obj2.mass * obj1.mass / r2
            # Проекции ускорения
            obj1.ax += F * dx / r / obj1.mass
            obj1.ay += F * dy / r / obj1.mass


def update(objects, dt, steps):
    compute_accelerations(objects)

    for _ in range(steps):
        old_acc = [(obj.ax, obj.ay) for obj in objects if not obj.fixed]

        for obj in objects:
            if not obj.fixed:
                obj.x += obj.vx * dt + 0.5 * obj.ax * dt * dt
                obj.y += obj.vy * dt + 0.5 * obj.ay * dt * dt

        compute_accelerations(objects)

        idx = 0
        for obj in objects:
            if not obj.fixed:
                ax_old, ay_old = old_acc[idx]
                obj.vx += 0.5 * (ax_old + obj.ax) * dt
                obj.vy += 0.5 * (ay_old + obj.ay) * dt
                idx += 1
