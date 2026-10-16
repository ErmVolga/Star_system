from math import hypot


def kinetic_energy(objects):
    E = 0.0
    for o in objects:
        if not o.fixed:
            E += 0.5 * o.mass * (o.vx ** 2 + o.vy ** 2)
    return E


def potential_energy(objects, G):
    E = 0.0
    for i, a in enumerate(objects):
        for b in objects[i + 1:]:
            r = hypot(b.x - a.x, b.y - a.y)
            if r > 0:
                E -= G * a.mass * b.mass / r
    return E


def total_energy(objects, G):
    return kinetic_energy(objects) + potential_energy(objects, G)