from settings import WIDTH, HEIGHT, SCALE, AU


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.scale = SCALE
        self.width = WIDTH
        self.height = HEIGHT

        self.keyboard_speed = 5 * AU

    def world_to_screen(self, pos):
        return (
            (pos[0] - self.x) / self.scale + self.width / 2,
            (pos[1] - self.y) / self.scale + self.height / 2
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def drag(self, dx, dy):
        self.x -= dx * self.scale
        self.y -= dy * self.scale