from scripts.variables.localvars import *


class BlinkingTile:

    def __init__(self, surface, range=(25, 150, 10)):

        self.surface = surface

        # The range specifies the way it should step through opacities, range[0] is the starting opacity and the minimum
        # level, range[1] is the ending opacity and the maximum value, range[2] is the step value of the loop per second
        self.min = range[0]
        self.max = range[1]
        self.step = range[2]

        # The actual value for the opacity of the surface
        self.opacity = self.min

        # Is opacity increasing or decreasing
        self.increasing = True

    def update(self, engine):
        if engine.game_vars[FPS]:
            delta_time = 1 / engine.game_vars[FPS]
        else:
            delta_time = 0
        diff = delta_time * self.step

        if self.increasing:
            self.opacity = min(self.opacity + diff, self.max)
            if self.opacity >= self.max:
                self.increasing = False
        else:
            self.opacity = max(self.opacity - diff, self.min)
            if self.opacity <= self.min:
                self.increasing = True

    def render(self):
        self.surface.set_alpha(self.opacity)
        self.surface.convert()
        return self.surface

    def get_width(self):
        return self.surface.get_width()
