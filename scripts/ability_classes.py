from scripts.variables.events import *
from scripts.ability_sounds import *
from scripts import Astar

"""

ability_classes.py class

constructor function for abilities

supported types:
light
heavy
block
shields
dots
hots
knockbacks
aoe
tile_effects
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

class Ability:

    def __init__(self, name, actions, flags=None, uses=1, k_message=None, sound_pack=snd_empty_pack, range=1):
        self.name = name

        if actions is None:
            self.actions = []
        else:
            self.actions = actions

        if flags is None:
            self.flags = []
        else:
            self.flags = flags

        self.type = None
        self.uses = uses

        if k_message:
            self.kill_message = k_message
        else:
            self.kill_message = "{0} kills {1}!"

        self.s_sound = sound_pack.success_sound
        self.f_sound = sound_pack.failure_sound
        self.p_sound = sound_pack.partial_sound

        self.range = range

    def __str__(self):
        return "[{}]".format(self.name)

    def __repr__(self):
        return "[{}]".format(self.name)

    def afflict(self, attacker, target, outcome, engine):
        damage_dict = {}
        if not outcome["blocked"]:
            for action in self.actions:
                self.process_damage_dict(action.afflict(attacker, target, engine), damage_dict)
            for target, damage in damage_dict.items():
                if target.health > 0:
                    make_event(PRINT_LINE, message="{}'s [{}] did {} damage to {}.".format(attacker, self.name, damage, target))
                    make_event(PRINT_LINE, message="{} has {} health left.".format(target, target.health))
                else:
                    make_event(PRINT_LINE, message=self.kill_message.format(attacker, target))
        else:
            self.do_blocked_afflict(attacker, target, engine)

    @staticmethod
    def process_damage_dict(new_damage_dict, damage_dict):
        # Takes an incoming dict and "adds" it, so that the damage_dict holds the total damage done to each sprite
        for sprite, value in new_damage_dict.items():
            if damage_dict.get(sprite):
                damage_dict[sprite] += value
            else:
                damage_dict[sprite] = value

    def do_blocked_afflict(self, attacker, target, engine):
        # This can be overriden in subclasses to adjust the behavior of a blocked ability (i.e. if this attack is
        # blocked - then do these actions)
        # However it should NOT print blocked messages, that belongs to the ability responsible for the block
        pass

    def get_type(self):
        return self.type

    def is_in_range(self, attacker, target, grid):
        # Allows abilities to tell you if the can be used on the target or not
        if len(Astar.a_star(attacker.pos, target.pos, grid)) <= self.range or self.range == -1:
            return True
        return False


# ABILITIES

# PLACEHOLDER

class EmptyAttack(Ability):

    def __init__(self):
        super().__init__("EmptyAttack", None, range=-1)
        self.type = "empty_attack"

    def afflict(self, attacker, target, outcome, engine):
        make_event(PRINT_LINE, message="{} is out of range.".format(attacker))

# BLOCKS


class Block(Ability):

    def __init__(self, name, flags=None, uses=1, sound_pack=snd_empty_pack, actions=None):
        super().__init__(name, actions, flags, uses, sound_pack=sound_pack, range=-1)
        self.type = "block"

    def afflict(self, attacker, target, outcome, engine):
        super().afflict(attacker, target, outcome, engine)
        if outcome["blocking"]:
            make_event(PRINT_LINE, message="{} blocked {}'s [{}] ability with [{}]."
                       .format(attacker, target, outcome["opposite_ability"], self))
        else:
            make_event(PRINT_LINE, message="{}'s [{}] ability was ineffectual.".format(attacker, self))

    def can_block(self, ability):
        if "unblockable" in ability.flags:
            return False

        for flag in ability.flags:
            if flag in self.flags:
                return True
            return False


# MELEE ATTACKS

class MeleeAttack(Ability):

    def __init__(self, name, actions, flags=None, uses=1, k_message=None, sound_pack=snd_empty_pack, range=1):
        super().__init__(name, actions, flags, uses, k_message, sound_pack, range)
        self.type = "melee"

    # TODO: add logic for if it can reach or not, similar to Block's can_block method


class conditional_melee_attack(Ability):

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

class spell_attack(Ability):

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

class Action:

    def __init__(self):
        pass

    def afflict(self, attacker, target, engine):
        # Returns a dict with the damage done to each sprite
        # Damages the target(s)
        pass


class BasicDamage(Action):

    def __init__(self, damage):
        super().__init__()
        self.damage = damage

    def afflict(self, attacker, target, engine):
        # Damages a single mob
        total_damage = target.damage(attacker, self.damage)
        target.health_update()
        return {target: total_damage}


class OPDamage(Action):

    def __init__(self):
        super().__init__()

    def afflict(self, attacker, target, engine):
        total_damage = target.damage(attacker, target.health + 1)
        target.health_update()
        return {target: total_damage}


class basicAoE(Action):

    def __init__(self, name, damage, grid, pos):
        super().__init__()
        self.damage = damage
        self.grid = grid

    def afflict(self, target):
        pass


class buff(Action):

    def __init__(self, name, effect=hot("Dummy Spell", 1, 2, 0)):
        super().__init__()
        self.effect = effect

    def afflict(self, target):
        self.effect.apply(target)


class debuff(Action):

    def __init__(self, name, effect=dot("Dummy Spell", -1, 2, 0)):
        self.effect = effect

    def afflict(self, target):
        self.effect.apply(target)


class empty_attack(Action):

    def __init__(self):
        super().__init__("empty")

    def afflict(self, target):
        print(self.playername + " stares blankly, it does nothing.")
