from pygame.mixer import Sound
import pygame


"""
Holds all of the sounds that abilities can play
"""

pygame.mixer.init()


class SoundPack:

    def __init__(self, s_sound, f_sound, p_sound):

        # Allows all three sounds to be passed as one parameter to an Ability class

        self.success_sound = s_sound
        self.failure_sound = f_sound
        self.partial_sound = p_sound


basic_sword = Sound("sounds/fight/sword_clash.wav")
eerie_magic = Sound("sounds/fight/eerie_magic.wav")
block = Sound("sounds/fight/shield_block.wav")


snd_basic_atk = SoundPack(basic_sword, None, None)
snd_basic_mag = SoundPack(eerie_magic, None, None)
snd_basic_blk = SoundPack(block, None, None)
snd_empty_pack = SoundPack(None, None, None)


