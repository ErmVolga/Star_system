from physics.body import *
from settings import *

Sun = SpaceObject("Солнце", 0, 0, 0, 0, YELLOW, 30, 332940 * EARTH_MASS, True)
Mercury = SpaceObject("Меркурий", 0.466697 * AU, 0, 0, -38860, GREY, 10, 0.055274 * EARTH_MASS)
Venus = SpaceObject("Венера", 0.728213 * AU, 0, 0, -34790, BEIGE, 10, 0.815 * EARTH_MASS)
Earth = SpaceObject("Земля", 1.0167086 * AU, 0, 0, -29290, BLUE, 10, EARTH_MASS)
Moon = SpaceObject("Луна", Earth.x + 405400000, 0, 0, Earth.vy + 964, WHITE, 2, EARTH_MASS / 81.3)
Mars = SpaceObject("Марс", 1.66621 * AU, 0, 0, -21970, RED, 10, 0.107 * EARTH_MASS)
Jupiter = SpaceObject("Юпитер", 5.458104 * AU, 0, 0, -13070, ORANGE, 10, 317.8 * EARTH_MASS)

objects = [Sun, Earth, Moon, Mercury, Venus, Mars, Jupiter]
