from settings import CENTER_X, CENTER_Y

class Camera:
    def __init__(self):
        self.x = CENTER_X
        self.y = CENTER_Y

    def world_to_screen(self, pos):
        return (
            pos[0] - self.x,
            pos[1] - self.y
        )

    def screen_to_world(self, pos):
        return (
            pos[0] + self.x,
            pos[1] + self.y

        )