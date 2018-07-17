from scripts.ability import *
from scripts import sprite_ai
#import scripts.gui_elements.DisplayWindow

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
        self.abilities = [melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light"))]

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

    def use(self, abilitypos, target, ability=None):
        if ability:
            ability.afflict(target)
        else:
            if abilitypos > len(self.abilities):
                make_event(PRINT_LINE, message=self.name + " doesn't have enough abilities...")
                self.abilities[-1].afflict(target)
            else:
                self.abilities[abilitypos].afflict(target)

    def choose_ability(self, pos):
        return pos

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

    def dodamage(self, source, value):
        self.health -= value

    def dohealing(self, value):
        self.health += value


class Player(Sprite):

    def __init__(self, name, pclass, picloc, pos):
        super().__init__(name, pclass, picloc, pos)
        self.type = "player"
        if pclass.lower() == "warrior":
            self.abilities = ["light", "light", "heavy", "sweep", "block", "parry", "counter"]
        if pclass.lower() == "tank":
            self.abilities = [melee_attack("Execute", self, (basic_damage("", 5),), ("heavy"), uses=3),
                              melee_attack("OP BS", self, (op_damage(""),), ("magic"),
                                           "{1} is killed by the architects!"),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                              melee_attack("Execute", self, (basic_damage("", 5),), ("heavy"), uses=3),
                              melee_attack("OP BS", self, (op_damage(""),), ("magic"),
                                           "{1} is killed by the architects!"),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                              melee_attack("Light", self, (basic_damage("", 1),), ("light"))
                              ]

    def choose_ability(self, pos):
        choice = int(input("Choose an ability to use (1-{}): ".format(str(len(self.abilities)))))
        return choice - 1


class Monster(Sprite):
    def __init__(self, name, class_, picloc, pos, abilities=[]):
        super().__init__(name, class_, picloc, pos)
        self.type = "monster"
        self.threattable = {None: 0}
        self.target = None
        self.speed = 4
        self.health = 20
        self.abilities = [melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light")),
                          melee_attack("Light", self, (basic_damage("", 1),), ("light"))]

        self.AI = sprite_ai.BaseMonsterAI(self)

    def dodamage(self, source, value):
        super().dodamage(source, value)
        if source not in self.threattable:
            self.threattable[source] = value
        else:
            self.threattable[source] = self.threattable[source] + value
        if self.threattable[source] > self.threattable[self.target]:
            self.target = source

    def get_target(self):
        return self.target

    def set_target(self, target):
        self.target = target