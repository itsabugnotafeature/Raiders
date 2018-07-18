import pygame


class SFXPlayer:

    def __init__(self, sprite):

        self.sprite = sprite
        self.default_ability_sound = pygame.mixer.Sound("sounds/fight/sword_clash.wav")

    def use(self, ability, audio_player):

        try:
            audio_player.play(ability.sound)
        except AttributeError:
            print("Error playing sound for {}'s [{}] ability, no sound found".format(self.sprite.name, ability))
            print("Reverting to default sound.")
            audio_player.play_sound(self.default_ability_sound, channel_set="fight")
