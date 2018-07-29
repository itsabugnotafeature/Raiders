from scripts.variables.localvars import *
from systems.BaseSystem import BaseSystem
from scripts import channel_manager


class GameAudio(BaseSystem):

    def __init__(self):
        self.Engine = None
        self.game_vars = []

        self.ChannelManager = channel_manager.ChannelManager(8)

    def play(self, sound, priority=HIGH):
        channel_id, queued = self.ChannelManager.play(sound, priority)
        return channel_id, queued

    def stop(self, channel_id, sound=None):
        self.ChannelManager.stop(channel_id, sound)

    def get_sound(self, channel_id):
        return self.ChannelManager.get_sound(channel_id)
