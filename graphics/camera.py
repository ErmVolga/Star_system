from settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

        self.width = WIDTH
        self.height = HEIGHT

    def world_to_screen(self, pos):
        return (
            (pos[0] - self.x) + self.width / 2,
            (pos[1] - self.y) + self.height / 2
        )

    def screen_to_world(self, pos):
        return (
            pos[0] + self.x,
            pos[1] + self.y

        )