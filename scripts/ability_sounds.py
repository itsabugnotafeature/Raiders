from pygame.mixer import Sound
import pygame
from scripts.tools import os_format_dir_name


"""
Holds all of the sounds that abilities can play
"""

pygame.mixer.init()


class SoundPack:

    def __init__(self, s_sound, f_sound, p_sound):

        # Allows all three sounds to be passed as one parameter to an Ability class

        self.success_sound_file = s_sound
        self.failure_sound_file = f_sound
        self.partial_sound_file = p_sound


basic_sword = os_format_dir_name("sounds{os_dir}fight{os_dir}sword_clash.wav")
eerie_magic = os_format_dir_name("sounds{os_dir}fight{os_dir}eerie_magic.wav")
block = os_format_dir_name("sounds{os_dir}fight{os_dir}shield_block.wav")


snd_basic_atk = SoundPack(basic_sword, None, None)
snd_basic_mag = SoundPack(eerie_magic, None, None)
snd_basic_blk = SoundPack(block, None, None)
snd_empty_pack = SoundPack(None, None, None)


