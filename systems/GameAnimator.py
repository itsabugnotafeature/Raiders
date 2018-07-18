from scripts.variables.localvars import *
import scripts.animations
from systems.BaseSystem import BaseSystem


# TODO: add a combat idle animation
class Animator(BaseSystem):

    def __init__(self):
        self.animation_dict = {}
        self.Engine = None

    def set_engine(self, new_engine):
        self.Engine = new_engine
        return True

    def set_up(self):
        for sprite in self.Engine.game_vars[SPRITE_LIST]:
            self.animation_dict[sprite] = scripts.animations.standby()
            # Copy does exactly what you'd expect
            # this way the sprites don't point to
            # the same Animation object

    def init(self, engine):
        self.set_engine(engine)
        self.set_up()

    def main_loop(self):
        if self.Engine.game_vars[FPS] and not self.Engine.game_vars[PAUSE]:
            delta_time = 1 / self.Engine.game_vars[FPS]
            for player in self.animation_dict:
                animation_state = self.animation_dict[player].tick(delta_time)
                if animation_state is not None:
                    player.animation_state = animation_state
                    player.did_tick = True

    def set_animation(self, sprite, animation):
        self.animation_dict[sprite] = animation

    def remove_sprite(self, sprite):
        self.animation_dict.pop(sprite)
