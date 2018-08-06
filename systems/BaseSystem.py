"""
Provides an abstract class for any system that wants to work with the GameEngine
"""


class BaseSystem:

    def __init__(self):
        self.Engine = None
        self.game_vars = {}

    def set_engine(self, new_engine):
        self.Engine = new_engine

    def set_up(self):
        self.game_vars = self.Engine.game_vars

    def init(self, engine):
        self.set_engine(engine)
        self.set_up()

    def main_loop(self):
        pass
