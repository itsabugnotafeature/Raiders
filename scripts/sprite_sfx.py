import pygame


class SFXPlayer:

    def __init__(self, sprite):

        self.sprite = sprite
        self.default_ability_sound = pygame.mixer.Sound("sounds/fight/sword_clash.wav")

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
                self.play_sound(sound, audio_player, ability.name)
            else:
                print("AUDIO: No sound for {}'s [{}] ability with outcome {}.".format(self.sprite, ability, outcome))

        except AttributeError:
            print("AUDIO: No sound found for {}'s [{}] ability.".format(self.sprite, ability))
        except TypeError:
            print("AUDIO: No sound found for {}'s [{}] ability.".format(self.sprite, ability))

    def play_default_sound(self, ability, audio_player):
        channel_id, queued = audio_player.play(self.default_ability_sound)
        print("SOUND: Error playing sound for {}'s [{}] ability, no sound found".format(self.sprite.name, ability))
        print("SOUND: Reverting to default sound on channel {}.".format(channel_id))

    def play_sound(self, sound, audio_player, name):
        channel_id, queued = audio_player.play(sound)
        if queued:
            print("AUDIO: Sound for {}'s [{}] ability queued on channel {}.".format(self.sprite.name, name,
                                                                                    channel_id))
        else:
            print(("AUDIO: Playing sound for {}'s [{}] ability on channel {}.".format(self.sprite.name, name,
                                                                                      channel_id)))
