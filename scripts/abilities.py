from scripts.ability_classes import *
from scripts.ability_sounds import *


"""
Provides the instances of abilities that can be used by sprites
"""


dmg_light_01 = MeleeAttack("Light", [BasicDamage(1)], ["light"], 1, "{0} slashes {1} to death!", snd_basic_atk)
dmg_light_02 = MeleeAttack("Light", [BasicDamage(1)], ["light"], 2, "{0} slashes {1} to death!", snd_basic_atk)
dmg_execute_01 = MeleeAttack("Execute", [BasicDamage(5)], ["heavy"], 3, "{0} snaps {1}'s neck!", snd_basic_atk)
dmg_op_01 = MeleeAttack("OP", [OPDamage()], ["unblockable"], 1, "{1} mysteriously vanishes...", snd_basic_mag, range=3)
dmg_light_ub_01 = MeleeAttack("Light", [BasicDamage(1)], ["light", "unblockable"], 2, "{0} slashes {1} to death!", snd_basic_atk)
blk_basic_01 = Block("Block", ["light", "heavy"], 1, snd_basic_blk)
blk_light_01 = Block("Parry", ["light"], 1, snd_basic_blk)
empty_atk = EmptyAttack()
