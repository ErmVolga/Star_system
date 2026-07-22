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

    def __str__(self):
        return f"{self.name}: x={self.x:.2f}, y={self.y:.2f}"
