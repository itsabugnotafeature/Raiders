from scripts.ability import *
from scripts import sprite_ai
from scripts import sprite_threat
from scripts import animations
from scripts.Colors import Color
from scripts import tools
from scripts import sprite_animator
from scripts import sprite_sfx

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
        self.abilities = [melee_attack("Light", self, (basic_damage("", 1),), ("light",)),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light",)),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light",))]

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
        self.SFXPlayer = sprite_sfx.SFXPlayer(self)

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

    def use(self, abilitypos, target, engine):
        if self.fightable:

            # The chosen ability
            active_ability = self.get_attack(abilitypos)

            # TODO: .afflict() should return a boolean to tell if
            active_ability.afflict(target)
            self.SpriteAnimator.use(active_ability, engine.Animator)
            self.SFXPlayer.use(active_ability, engine.Audio)
        else:
            make_event(PRINT_LINE, message="{} can't attack while dead.".format(self.name), color=Color.Red)

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

    def heal(self, value):
        self.health += value

    def face(self, pos):
        self.facing = tools.get_facing(self.pos, pos, self.facing)

    def get_attack(self, ability_pos):
        try:
            active_ability = self.abilities[ability_pos]
        except IndexError:
            active_ability = self.abilities[0]
            print("Error using {}'s [{}] ability, reverting to number 1.".format(self.name, active_ability.name))
        return active_ability


class Player(Sprite):

    def __init__(self, name, pclass, picloc, pos):
        super().__init__(name, pclass, picloc, pos)
        self.type = "player"
        if pclass.lower() == "warrior":
            self.abilities = ["light", "light", "heavy", "sweep", "block", "parry", "counter"]
        if pclass.lower() == "tank":
            self.abilities = [melee_attack("Execute", self, (basic_damage("", 5),), ("heavy",), uses=3),
                              melee_attack("OP BS", self, (op_damage(""),), ("magic",),
                                           "{1} is killed by the architects!"),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light",), uses=3),
                              melee_attack("Execute", self, (basic_damage("", 5),), ("heavy",), uses=3),
                              melee_attack("OP BS", self, (op_damage(""),), ("magic",),
                                           "{1} is killed by the architects!"),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light",)),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light",))
                              ]

    def choose_ability(self, pos):
        choice = int(input("Choose an ability to use (1-{}): ".format(str(len(self.abilities)))))
        return choice - 1


class Monster(Sprite):
    def __init__(self, name, class_, picloc, pos, abilities=None):
        super().__init__(name, class_, picloc, pos)
        self.type = "monster"
        self.target = None
        self.speed = 4
        self.health = 20

        # Both of these ability lists should be exactly 3 items long and contain only Ability classes
        if abilities is not None:
            self.threat_abilities = abilities[0:3]
            self.no_threat_abilities = abilities[3:6]
        else:

            self.threat_abilities = [melee_attack("Execute", self, (basic_damage("", 5),), ("heavy",), uses=3),
                                     melee_attack("Execute", self, (basic_damage("", 5),), ("heavy",), uses=3),
                                     melee_attack("Execute", self, (basic_damage("", 5),), ("heavy",), uses=3)]
            self.no_threat_abilities = [melee_attack("Light", self, (basic_damage("", 1),), ("light",)),
                                        melee_attack("Light", self, (basic_damage("", 1),), ("light",)),
                                        melee_attack("Light", self, (basic_damage("", 1),), ("light",))]

        self.AI = sprite_ai.BaseMonsterAI(self)
        self.ThreatManager = sprite_threat.ThreatManager(self)

    def damage(self, source, value):
        super().damage(source, value)
        self.target = self.ThreatManager.do_threat_update(source, value)

    # Ability_pos should always be the round number when using this method on an instance of Monster
    def use(self, ability_pos, target, engine):
        if self.fightable:
            active_ability = self.AI.get_attack(target, ability_pos, engine)

            active_ability.afflict(target)
            self.SpriteAnimator.use(active_ability, engine.Animator)
            self.SFXPlayer.use(active_ability, engine.Audio)

        else:
            make_event(PRINT_LINE, message="{} can't attack while dead.".format(self.name), color=Color.Red)

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target

    def get_move(self, grid, path_manager):
        return self.AI.do_move(grid, path_manager)
