from scripts.Astar import a_star
from scripts import sprite_classes
import random
from scripts import animations
from scripts.abilities import empty_atk

"""
The AI classes provide a collection of helpful decision makers for sprites.
Each method takes in some parameters and returns the desired object back to its sprite.
Possible subclasses:
    BossAI:
        provides support for multiple stages of abilities
    TimidAI:
        an AI that runs away under certain circumstances
    ConditionalAI:
        behaves like normal but if certain circumstances are met it will use preset abilities
"""


class BaseAI:

    def __init__(self, sprite):
        self.sprite = sprite

    def do_move(self, grid, path_manager):
        pass

    def get_attack(self, target, turn_num, grid):
        pass


class BaseMonsterAI(BaseAI):

    def __init__(self, monster, base_path=None):

        if isinstance(monster, sprite_classes.Monster):
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

    # Ability_pos should always be the turn number
    def get_attack(self, target, turn_num, grid):
        # TODO: consider making a SpriteAnimator class that the AI can delegate animation tasks to
        # Turn numbers start at 1 and go to 3 so we subtract to avoid IndexError
        turn_num -= 1

        try:
            if target == self.sprite.get_target():
                active_ability = self.sprite.threat_abilities[turn_num]
            else:
                active_ability = self.sprite.no_threat_abilities[turn_num]
        except IndexError:

            # TODO: let it use abilities with multiple uses
            active_ability = self.sprite.no_threat_abilities[0]
            print("Error using {}'s [{}] ability, reverting to number 1.".format(self.sprite, active_ability))

        if not active_ability.is_usable(self.sprite, target, grid, self.sprite.get_ability_uses(active_ability)):
            active_ability = empty_atk

        return active_ability
