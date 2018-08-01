import pygame
from scripts.Colors import Color
from scripts.variables.localvars import *


class Banner:

    def __init__(self, text, screen_dims, hang_time=5, theme=None, color=Color.Red):
        # Displays a text banner at the top of the screen and fades it out after time

        font = pygame.font.SysFont("lucidaconsole", 18, True)
        self.blit_img = font.render(text, False, color)

        self.width, self.height = self.blit_img.get_width(), self.blit_img.get_height()

        self.pos = ((screen_dims[0]-self.width)/2, 40)

        # Time is recorded in seconds
        # How long the banner has been displayed
        self.total_time = 0

        # How long the banner will hang on the screen
        self.hang_time = hang_time

        self.opacity = 255

    def render(self):
        self.blit_img.set_alpha(self.opacity)
        self.blit_img.convert()
        return self.blit_img

    def update(self, engine):
        if engine.game_vars[FPS]:
            delta_time = 1 / engine.game_vars[FPS]
        else:
            delta_time = 0
        # Add the time since last frame
        self.total_time += delta_time

        if self.total_time > self.hang_time:
                return None
        return self
