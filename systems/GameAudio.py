from scripts.variables.localvars import *
from systems.BaseSystem import BaseSystem


class GameAudio(BaseSystem):

    def __init__(self):
        self.Engine = None
        self.game_vars = []

        self.base_channel = None
        self.fight_channel1 = None
        self.fight_channel2 = None
        self.back_music_channel1 = None
        self.back_music_channel2 = None
        self.gui_channel = None
        self.sound_effect_channel1 = None
        self.sound_effect_channel2 = None
        self.sound_effect_channel3 = None
        self.sound_effect_channel4 = None
        self.misc_channel1 = None
        self.misc_channel2 = None
        self.misc_channel3 = None
        self.misc_channel4 = None

        self.fight_channels = []
        self.back_music_channels = []
        self.sound_effect_channels = []
        self.misc_channels = []

        self.all_channels = []

    def init(self, engine):
        self.set_engine(engine)
        self.set_up()

    def set_engine(self, new_engine):
        self.Engine = new_engine

    def set_up(self):
        self.init_channels()

    def main_loop(self):
        pass

    def init_channels(self):
        pygame.mixer.set_num_channels(14)

        self.base_channel = pygame.mixer.Channel(0)
        self.fight_channel1 = pygame.mixer.Channel(1)
        self.fight_channel2 = pygame.mixer.Channel(2)
        self.back_music_channel1 = pygame.mixer.Channel(3)
        self.back_music_channel2 = pygame.mixer.Channel(4)
        self.gui_channel = pygame.mixer.Channel(5)
        self.sound_effect_channel1 = pygame.mixer.Channel(6)
        self.sound_effect_channel2 = pygame.mixer.Channel(7)
        self.sound_effect_channel3 = pygame.mixer.Channel(8)
        self.sound_effect_channel4 = pygame.mixer.Channel(9)
        self.misc_channel1 = pygame.mixer.Channel(10)
        self.misc_channel2 = pygame.mixer.Channel(11)
        self.misc_channel3 = pygame.mixer.Channel(12)
        self.misc_channel4 = pygame.mixer.Channel(13)

        self.fight_channels = [self.fight_channel1, self.fight_channel2]
        self.back_music_channels = [self.back_music_channel1, self.back_music_channel2]
        self.sound_effect_channels = [self.sound_effect_channel1, self.sound_effect_channel2,
                                      self.sound_effect_channel3, self.sound_effect_channel4]
        self.misc_channels = [self.misc_channel1, self.misc_channel2, self.misc_channel3, self.misc_channel4]

        self.all_channels = [self.base_channel, *self.fight_channels, *self.back_music_channels,
                             self.gui_channel, *self.sound_effect_channels, *self.misc_channels]

        self.set_channels_volumes()

    def set_channels_volumes(self, volume=None, **kwargs):

        for channel in self.all_channels:
            if volume is None:
                channel.set_volume(.5, .5)
            else:
                channel.set_volume(volume, volume)

        for key, value in kwargs:
            self.all_channels[key].set_volume(value)

    def play(self, sound, channel_set=None, priority=-1):
        # channel_set lets you pick what list of channels to play from, defaults to self.misc_channels
        # it will find the first channel that isn't busy, failing that it will find the first channel that isn't queued,
        # failing that, if your priority is greater than 0 it will force it to play on the respective channel in that
        # channel set (the higher the priority the less likely to be overridden), otherwise the sound won't play and
        # an error message will print out.
        if channel_set in [None, "misc", 3, "3", "-1", -1]:
            channel, force = self.get_open_channel(self.misc_channels, priority)
        elif channel_set in ["fight", "fight_channels", 0, "0"]:
            channel, force = self.get_open_channel(self.fight_channels, priority)
        elif channel_set in ["back", "music", 1, "1", "back_music", "back_music_channels"]:
            channel, force = self.get_open_channel(self.back_music_channels, priority)
        elif channel_set in ["sfx", "sound_effect_channels", 2, "2", "sound_effect"]:
            channel, force = self.get_open_channel(self.sound_effect_channels, priority)
        elif channel_set in["base", "base_channel"]:
            channel, force = self.base_channel, not self.base_channel.busy()
        else:
            channel, force = self.get_open_channel(self.misc_channels, priority)

        if force and channel:
            channel.play(sound)
            return self.all_channels.index(channel)
        elif channel:
            channel.queue(sound)
            return self.all_channels.index(channel)
        else:
            print("AUDIO: Error finding channel in channel set '{}' with priority {}".format(channel_set, priority))
            print("AUDIO: Not playing {}".format(sound))
            return None

    def get_open_channel(self, channel_set, priority):
        for c in channel_set:
            if not c.get_busy():
                return c, True
        else:
            for c in channel_set:
                if not c.get_queue():
                    return c, False
            else:
                if priority > 0:
                    return channel_set[max(-len(channel_set), -priority)], True
                else:
                    return False, False
