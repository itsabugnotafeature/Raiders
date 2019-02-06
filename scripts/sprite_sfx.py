import pygame
from scripts.tools import os_format_dir_name


class SFXPlayer:

    def __init__(self, sprite):

        self.sprite = sprite
        self.default_ability_sound = os_format_dir_name("sounds{os_dir}fight{os_dir}sword_clash.wav")

    def use(self, ability, outcome,  audio_player):

        try:

            if ability.type == "block":
                if outcome["blocking"]:
                    sound = ability.s_sound
                else:
                    sound = ability.f_sound
            else:
                if not outcome["blocked"]:
                    sound = ability.s_sound
                else:
                    sound = ability.f_sound

            if sound is not None:
                self.play_sound(sound, audio_player, ability)
            else:
                print("AUDIO: No sound for {}'s {} ability with outcome {}.".format(self.sprite, ability, outcome))

        except AttributeError:
            print("AUDIO: No sound found for {}'s {} ability.".format(self.sprite, ability))
        except TypeError:
            print("AUDIO: No sound found for {}'s {} ability.".format(self.sprite, ability))

    def play_sound(self, sound, audio_player, ability):
        stream_hash = audio_player.play(sound)
        print(("AUDIO: Playing sound for {}'s {} ability on stream {}.".format(self.sprite.name, ability, stream_hash)))
