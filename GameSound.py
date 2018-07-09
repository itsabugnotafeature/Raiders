from scripts.variables.localvars import *


class GameSound:

    def __init__(self):
        self.Engine = None
        self.game_vars = []
        self.fight_sound = pygame.mixer.Sound("sounds//fight//sword_clash.wav")
        self.fight_sound.set_volume(.3)

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

    def handle_event(self, event):
        if event.type == FIGHT_EVENT:
            if event.subtype == ACTION:
                self.fight_channel1.play(self.fight_sound, 0, 1300, 50)

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

    def set_channels_volumes(self, **kwargs):

        for channel in self.all_channels:
            channel.set_volume(.5, .5)

        for key, value in kwargs:
            self.all_channels[key].set_volume(value)
