from settings import WIDTH, HEIGHT, SCALE


class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.width = WIDTH
        self.height = HEIGHT

    def world_to_screen(self, pos):
        return (
            (pos[0] - self.x) / SCALE + self.width / 2,
            (pos[1] - self.y) / SCALE + self.height / 2
        )
