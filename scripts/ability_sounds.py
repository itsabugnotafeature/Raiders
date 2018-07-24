from pygame.mixer import Sound
import pygame


"""
Holds all of the sounds that abilities can play
"""

pygame.mixer.init()

snd_basic_sword = Sound("sounds/fight/sword_clash.wav")
snd_eerie_magic = Sound("sounds/fight/eerie_magic.wav")
snd_block = Sound("sounds/fight/shield_block.wav")


class SoundPack:

    def __init__(self, s_sound, f_sound, p_sound):

        # Allows all three sounds to be passed as one parameter to an Ability class

        self.success_sound = s_sound
        self.failure_sound = f_sound
        self.partial_sound = p_sound
