from scripts.Astar import a_star
from scripts import sprite_class
import random


class BaseAI:

    def __init__(self, sprite):
        self.abilities = sprite.abilities
        self.sprite = sprite

    def do_move(self, grid, path_manager):
        pass

    def do_attack(self, defender, round_num):
        pass


class BaseMonsterAI(BaseAI):

    def __init__(self, monster, base_path=None):

        if isinstance(monster, sprite_class.Monster):
            super().__init__(monster)
        else:
            raise Exception("MonsterAI must be init-ed with Monster class, not {}".format(str(monster)))

        # Specifies a path for the monster to walk otherwise it will be randomly generated
        self.base_path = base_path

        self.last_goal = monster.pos

    def do_move(self, grid, path_manager):

        sprite_target = self.sprite.get_target()
        if sprite_target is not None:
            path = a_star(self.sprite.pos, sprite_target.pos, grid)
        else:
            if not path_manager.contains_sprite(self.sprite):
                path_manager.add_monster(self.sprite, path=self.base_path)
            goal = path_manager.get_next_step(self.sprite)

            # If the AI recognizes that it has tried to go here before it reverses the path and tries again

            if self.evaluate_goal(goal):
                path = a_star(self.sprite.pos, goal, grid)
            else:
                path_manager.reverse_path(self.sprite)
                goal = path_manager.get_next_step(self.sprite)
                path = a_star(self.sprite.pos, goal, grid)

        # Trimmed so that the sprite never moves father than it actually can
        path = path[:self.sprite.speed + 1]
        return path

    # Used to stop sprites from getting caught on walls
    def evaluate_goal(self, spot):
        if spot == self.last_goal:
            return False
        else:
            self.last_goal = spot
            return True

    # Ability_pos should always be the round number
    def do_attack(self, target, ability_pos):

        self.sprite.use(round_num, defender)
