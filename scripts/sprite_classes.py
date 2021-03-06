from scripts.abilities import *
from scripts import sprite_ai
from scripts import sprite_threat
from scripts.Colors import Color
from scripts import tools
from scripts import sprite_animator
from scripts import sprite_sfx
from scripts import sprite_ability_manager

# TODO: generate getter/setter methods for all traits so that abilities can edit/reset them


class Sprite:

    def __init__(self, name, class_, picloc, pos):

        # METADATA
        self.name = name
        self.class_ = class_
        self.speed = 5
        self.health = 20
        self.maxhealth = self.health
        self.weakness = 0
        self.effects = []
        self.fightable = True
        self.abilities = [dmg_light_02, dmg_light_02, dmg_light_02]

        # DRAWING ITSELF
        img = pygame.image.load("graphics//Sprites//" + picloc)
        self.img_list = [[], [], [], [], [], []]
        for i in range(6):
            for j in range(4):
                surface = pygame.Surface((80, 80))
                surface.blit(img, (0, 0), (i*80, j*80, 80, 80))
                surface.set_colorkey((255, 255, 255))
                surface.convert()
                self.img_list[i].append(surface)
        self.animation_state = 0
        self.facing = 0
        self.pos = pos
        self.last_pos = self.pos
        self.offset = (0, -28)

        self.name_img = pygame.Surface((80, 80))

        # ANIMATION LOGIC
        self.did_tick = False
        self.SpriteAnimator = sprite_animator.SpriteAnimator(self)

        # SOUND
        self.SFXPlayer = sprite_sfx.SFXPlayer(self)

        # FIGHT LOGIC
        self.AbilityManager = sprite_ability_manager.AbilityManager(self)

    def render_name(self, font, theme):
        self.name_img = font.render(self.name, False, theme.accent3)

    def draw(self):
        return self.img_list[self.animation_state][self.facing]

    def ticked(self):
        if self.did_tick:
            self.did_tick = False
            return True
        else:
            return False

    def use(self, active_ability, target, outcome, engine):
        if outcome["death_blocked"]:
            make_event(PRINT_LINE, message="{} can't attack while dead.".format(self.name), color=Color.DarkRed)
        else:
            active_ability.afflict(self, target, outcome, engine)
            # TODO: add sprite blocking and blocked animations
            self.SpriteAnimator.use(active_ability, outcome, engine.Animator)
            self.SFXPlayer.use(active_ability, outcome, engine.Audio)
            self.AbilityManager.use(active_ability)

    def can_make_attack(self, target, grid):
        # Checks to see if the sprite can use any of its abilities
        # Used once per turn
        return self.AbilityManager.can_make_attack(target, grid)

    def prepare_for_fight(self):
        # Provides access to AbilityManger.start_fight and any other systems that want to be notified
        self.AbilityManager.start_fight()

    def prepare_for_turn(self):
        # Provides access to AbilityManger.start_turn and any other systems that want to be notified
        self.AbilityManager.start_turn()

    def get_ability_uses(self, ability):
        # Exposes the AbilityManager.get_ability_uses method
        return self.AbilityManager.get_ability_uses(ability)

    def is_ability_usable(self, ability, target, grid):
        # Exposes the AbilityManager.is_ability_usable method
        return self.AbilityManager.is_ability_usable(ability, target, grid)

    def health_update(self):
        if self.health <= 0:
            self.health = 0
            self.fightable = False
            return False
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def damage(self, source, value):
        self.health -= value
        return value

    def heal(self, value):
        self.health += value

    def face(self, pos):
        self.facing = tools.get_facing(self.pos, pos, self.facing)


class Player(Sprite):

    def __init__(self, name, pclass, picloc, pos):
        super().__init__(name, pclass, picloc, pos)
        self.type = "player"
        if pclass.lower() == "warrior":
            self.abilities = [blk_light_01, dmg_light_01, dmg_op_01, dmg_execute_01, dmg_light_02, blk_basic_01]
        if pclass.lower() == "tank":
            self.abilities = [blk_light_01, dmg_light_01, dmg_op_01, dmg_execute_01, dmg_light_02, blk_basic_01]

    def choose_ability(self, pos):
        choice = int(input("Choose an ability to use (1-{}): ".format(str(len(self.abilities)))))
        return choice - 1

    # When using get_attack on any non Monster Sprite ability_num should be the index of the desired ability in that
    # sprites abilities list
    def get_attack(self, target, ability_num, grid):
        try:
            active_ability = self.abilities[ability_num]
        except IndexError:
            active_ability = self.abilities[0]
            print("Error using {}'s {} ability, reverting to number 1.".format(self.name, active_ability))
        return active_ability


class Monster(Sprite):
    def __init__(self, name, class_, picloc, pos, abilities=None):
        super().__init__(name, class_, picloc, pos)
        self.type = "monster"
        self.target = None
        self.speed = 4
        self.health = 20

        # Both of these ability lists should have only Ability classes,
        #  and those Ability's should have uses that add to 3
        if abilities is not None:
            self.abilities = abilities
            self.threat_abilities = abilities[0:3]
            self.no_threat_abilities = abilities[3:6]
        else:
            self.threat_abilities = [dmg_light_02, blk_basic_01]
            self.no_threat_abilities = [blk_basic_01, dmg_light_02]
            self.abilities = self.threat_abilities + self.no_threat_abilities

        self.AI = sprite_ai.BaseMonsterAI(self)
        self.ThreatManager = sprite_threat.ThreatManager(self)

    def damage(self, source, value):
        damage_done = super().damage(source, value)
        self.target = self.ThreatManager.do_threat_update(source, value)
        return damage_done

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target

    def get_move(self, grid, path_manager):
        return self.AI.do_move(grid, path_manager)

    # When using get_attack on an instance of Monster the first parameter should always be the turn number of the fight
    def get_attack(self, target, turn_num, grid):
        return self.AI.get_attack(target, turn_num, grid)

    def can_make_attack(self, target, grid):
        if target == self.get_target():
            for ability in self.threat_abilities:
                if ability.is_in_range(self, target, grid):
                    return True
        else:
            for ability in self.no_threat_abilities:
                if ability.is_in_range(self, target, grid):
                    return True
        return False
