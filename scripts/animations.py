import random


class SpriteAnimation:

    def __init__(self, *args, randomize=False, repetitions=-1):

        self.frame_list = []
        for arg in args:
            self.frame_list.append(arg)

        self.frame_pointer = 0
        self.time = 0
        self.randomize = randomize
        self.repetitions = repetitions * len(self.frame_list)

    def tick(self, delta_time):
        self.time += delta_time
        if self.randomize:
            self.time += (random.randint(0, 3) * .001)
        if self.frame_list[self.frame_pointer].get_duration() <= self.time:
            self.frame_pointer = (self.frame_pointer + 1) % len(self.frame_list)
            self.time = 0
            self.repetitions -= 1
            if self.repetitions == 0:
                self.frame_list = [Frame(0, 1.3), Frame(1, .5)]
                self.randomize = True
            animation_state = self.frame_list[self.frame_pointer].get_animation_state()
            return animation_state
        return None


class Frame:

    def __init__(self, animation_state, duration):

        self.animation_state = animation_state
        self.duration = duration

    def get_duration(self):
        return self.duration

    def get_animation_state(self):
        return self.animation_state


"""
Some default animations for the sprites
"""


def standby():
    return SpriteAnimation(Frame(0, 1.3), Frame(1, 1.5), randomize=True)


def run():
    return SpriteAnimation(Frame(4, .3), Frame(5, .3), randomize=True)


def attack():
    return SpriteAnimation(Frame(2, .3), Frame(3, .4), repetitions=1)
