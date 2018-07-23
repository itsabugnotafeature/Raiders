from scripts.variables.events import *

"""

ability.py class

constructor function for abilities

supported types:
light
heavy
block/negations
shields
dots
hots
knockback
aoe
effectplacing
spawning

flags:
unblockable
melee
ranged


for Wrath of the Elementals:
y  light/heavy
y  block
x  knockback
x  tile effects
y  DoTs
x  status effect interactions
y  status effects
y  conditional effects
x  summoning
x  soakable tile effects
x  AoE spells
x  Directional AoE
y  heals
x  taunt
x  shields
y  combos

"""


# MAIN CLASS FOR EFFECTS

class Effect:

    def __init__(self, name, duration=-1):
        self.name = name
        self.target = None
        self.type = None
        self.possessor = None
        self.duration = duration
        self.timer = 1

    def tick(self, target):
        print("this effect has no tick method")

    def __str__(self):
        return "Effect: " + str(self.name)

    def set_caster(self, caster):
        self.caster = caster

    def apply(self, target):
        self.possessor = target
        target.effects_list.append(self)

    def get_type(self):
        return self.type


class casting(Effect):

    def __init__(self, name, type, duration=3):
        super().__init__(name, duration)
        self.type = type

    def tick(self):
        self.possessor.speed = 0
        print(str(self.possessor) + " is casting.")
        if self.timer < self.duration or self.duration == -1:
            self.timer += 1
        else:
            target.effects_list.remove(self)


class dot(Effect):

    def __init__(self, name, duration, tickinterval, damagepertick):
        super().__init__(name, duration)
        self.type = "harmful"
        self.tickinterval = tickinterval
        self.damagepertick = damagepertick

    def update(self):
        if self.timer % self.tickinterval == 0:
            print(self.name + " did " + str(self.damagepertick) + " damage")
            self.possessor.damage(self.damagepertick)
        if self.timer < self.duration or self.duration == -1:
            self.timer += 1
        else:
            self.possessor.effects_list.remove(self)


class hot(Effect):

    def __init__(self, name, duration, tickinterval, healpertick):
        super().__init__(name, duration)
        self.type = "helpful"
        self.tickinterval = tickinterval
        self.healpertick = healpertick

    def update(self):
        if self.timer % self.tickinterval == 0:
            print(self.name + " healed for " + str(self.healpertick))
            self.possessor.heal(self.healpertick)
        if self.timer < self.duration or self.duration == -1:
            self.timer += 1
        else:
            self.possessor.effects_list.remove(self)


# MAIN CLASS FOR ABILITIES

class ability():

    def __init__(self, name, possessor, actions, flags=(), uses=1):
        self.name = name
        self.flags = flags
        self.possessor = possessor
        self.actions = actions
        self.type = None
        self.uses = uses
        for action in self.actions:
            action.setup(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def afflict(self, target):
        make_event(PRINT_LINE, message="This attack subclass has no afflict method!")

    def get_type(self):
        return self.type


# ABILITIES

# BLOCKS

class block(ability):

    def __init__(self, name, possessor, actions, flags=()):
        super().__init__(name, possessor, actions, flags)
        self.type = "block"

    def blocks(self, ability):
        for flag in ability.flags:
            if flag in self.flags:
                print(
                    self.possessor.name + "'s [" + self.name + "] blocked " + ability.possessor.name + "'s [" + ability.name + "]")
                return True
            return False

    def afflict(self, target):
        pass


# MELEE ATTACKS

class melee_attack(ability):

    def __init__(self, name, possessor, actions, flags=(), k_message=None, uses=1, sound=None):
        super().__init__(name, possessor, actions, flags, uses)
        self.type = "melee"
        if k_message:
            self.kill_message = k_message
        else:
            self.kill_message = "{0} slashes {1} to death!"

        self.sound = sound

    def afflict(self, target):
        for action in self.actions:
            action.afflict(target)
        if target.health > 0:
            make_event(PRINT_LINE, message=target.name + " has " + str(target.health) + " health left.")


class conditional_melee_attack(ability):

    def __init__(self, name, possessor, condition, actions=(), flags=()):
        super().__init__(name, possessor, actions, flags)
        self.condition = condition
        self.action1 = actions[0]
        if actions[1]:
            self.action2 = actions[1]
        else:
            self.action2 = None

    def afflict(self, target):
        if self.condition(target, self.possessor):
            self.action1.afflict(target)
        elif self.action2 is not None:
            self.action2.afflict(target)


# SPELL/RANGED ATTACKS [Unfinished]

class spell_attack(ability):

    def __init__(self, name, damage=1, casttime=0, abilities=(), flags=()):
        super().__init__(name, flags)
        self.user = user
        self.type = "spell"
        self.casttime = casttime
        self.damage = damage

    def afflict(self, target):
        print("Casting " + self.name + " in " + str(self.casttime) + " turns!")
        if casttime != 0:
            status_effect_casting().apply(self.possessor)


# ACTIONS

class action():

    def __init__(self, name):
        self.name = name
        self.possessor = None
        self.playername = None

    def setup(self, possessor):
        self.possessor = possessor
        self.playername = possessor.possessor.name
        if self.name == "":
            self.name = self.possessor.name
        if self.name[0] == "+":
            self.name = str(self.possessor.name + self.name[1:])


class basic_damage(action):

    def __init__(self, name, damage):
        super().__init__(name)
        self.damage = damage

    def afflict(self, target):
        make_event(PRINT_LINE, message=self.playername + "'s [" + self.name + "] did " + str(self.damage) + " damage to " + target.name + ".")
        target.damage(self.possessor.possessor, self.damage)
        target.health_update()


class op_damage(action):

    def __init__(self, name):
        super().__init__(name)

    def afflict(self, target):
        make_event(PRINT_LINE, message=self.playername + "'s [" + self.name + "] magically evaporated " + target.name + ".")
        target.damage(self.possessor.possessor, target.health + 1)
        target.health_update()


class basicAoE(action):

    def __init__(self, name, damage, grid, pos):
        super().__init__()
        self.damage = damage
        self.grid = grid

    def afflict(self, target):
        pass


class buff(action):

    def __init__(self, name, effect=hot("Dummy Spell", 1, 2, 0)):
        super().__init__()
        self.effect = effect

    def afflict(self, target):
        self.effect.apply(target)


class debuff(action):

    def __init__(self, name, effect=dot("Dummy Spell", -1, 2, 0)):
        self.effect = effect

    def afflict(self, target):
        self.effect.apply(target)


class empty_attack(action):

    def __init__(self):
        super().__init__("empty")

    def afflict(self, target):
        print(self.playername + " stares blankly, it does nothing.")
