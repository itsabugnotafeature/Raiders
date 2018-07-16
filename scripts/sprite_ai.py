from scripts.Astar import a_star
from scripts import sprite_class


class BaseAI:

    def __init__(self, sprite):
        self.abilities = sprite.abilities
        self.sprite = sprite

    def do_move(self, grid):
        pass

    def do_attack(self, defender, round_num):
        pass


class BaseMonsterAI(BaseAI):

    def __init__(self, monster):

        if isinstance(monster, sprite_class.Monster):
            super().__init__(monster)
        else:
            raise Exception("MonsterAI must be init-ed with Monster class, not {}".format(str(monster)))

    def do_move(self, grid):

        path = a_star(self.sprite.pos, self.sprite.get_target(), grid)
        return path

    def do_attack(self, defender, round_num):

        self.sprite.use(round_num, defender)
