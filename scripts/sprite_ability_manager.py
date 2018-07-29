from scripts.abilities import empty_atk


class AbilityManager:

    def __init__(self, sprite):
        """
        Keeps track of a sprite's abilities locally so that they can be queried to see if they can be used

        :param sprite: sprite_class.Sprite
        """
        self.sprite = sprite
        self.abilities = self.sprite.abilities

        # Sprite's abilities are keyed to the number of times it was used
        self.ability_uses = {empty_atk: 0}

    def start_fight(self):
        # Resets the uses dict for the fight and gets the current abilities for this sprite
        # Called once per fight on each sprite involved
        self.ability_uses.clear()
        self.ability_uses[empty_atk] = 0

        self.abilities = self.sprite.abilities[:]
        for ability in self.abilities:
            self.ability_uses[ability] = 0

    def start_turn(self):
        # Re-checks the sprite's abilities to keep  them up to date
        self.abilities = self.sprite.abilities[:]
        for ability in self.abilities:
            if ability not in self.ability_uses:
                self.ability_uses[ability] = 0

    def use(self, ability):
        self.ability_uses[ability] += 1

    def can_make_attack(self, target, grid):
        for ability in self.abilities:
            if self.is_ability_usable(ability, target, grid):
                return True
        return False

    def is_ability_usable(self, ability, target, grid):
        return ability.is_usable(self.sprite, target, grid, self.get_ability_uses(ability))

    def get_ability_uses(self, ability):
        return self.ability_uses[ability]
