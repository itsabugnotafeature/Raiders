import pygame


class SFXPlayer:

    def __init__(self, sprite):

        self.sprite = sprite
        self.default_ability_sound = pygame.mixer.Sound("sounds/fight/sword_clash.wav")

    def use(self, ability, audio_player):

        try:
            audio_player.play(ability.sound, channel_set="fight")
        except AttributeError:
            self.default_sound(ability, audio_player)
        except TypeError:
            self.default_sound(ability, audio_player)

    def default_sound(self, ability,  audio_player):
        channel_id = audio_player.play(self.default_ability_sound, channel_set="fight")
        print("SOUND: Error playing sound for {}'s [{}] ability, no sound found".format(self.sprite.name, ability))
        print("SOUND: Reverting to default sound on channel {}.".format(channel_id))
