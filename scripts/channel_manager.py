import time
import pygame
from scripts.variables.localvars import *


class ChannelManager:
    """
    Finds available channels to play sounds on.
    It uses priority and time to determine what should happen if there are no available channels
    """

    def __init__(self, total_channels=None):

        self.channel_list = []
        self.play_time_dict = {}

        self.init_channels(total_channels)

    def init_channels(self, num_channels=None):

        if num_channels is not None and num_channels > 0:
            pygame.mixer.set_num_channels(num_channels)

        for channel_id in range(pygame.mixer.get_num_channels()):
            self.channel_list.append(pygame.mixer.Channel(channel_id))

        for channel in self.channel_list:
            self.play_time_dict[channel] = time.time()

    def play(self, sound, priority):
        # HIGH guarantees that the sound will be played, if there are no available it plays it on the channel that was
        # queued/played the longest time ago
        # MEDIUM guarantees that the sound will at least be queued on the channel that was queued/played the longest ago
        # LOW tries to queue/play the sound with no guarantees
        # Returns the id of the channel selected (which is its index in channels_list) and a boolean for queued or not
        for channel in self.channel_list:
            if not channel.get_busy():
                channel.play(sound)
                self.play_time_dict[channel] = time.time()
                return self.channel_list.index(channel), False

        if priority == HIGH:
            self.channel_list[0].play(sound)
            self.play_time_dict[self.channel_list[0]] = time.time()
            # channel_list is sorted on every play() call, so this always plays on the channel that was queued/played
            # the longest ago
            return 0, False

        for channel in self.channel_list:
            if channel.get_queue() is None:
                channel.queue(sound)
                self.play_time_dict[self.channel_list[0]] = time.time()
                return self.channel_list.index(channel), True

        if priority == MEDIUM:
            self.channel_list[0].queue(sound)
            self.play_time_dict[self.channel_list[0]] = time.time()
            return 0, True

        if priority == LOW:
            print("AUDIO: No channel found for {}.".format(sound))
            return -1, False

        self.sort_channel_list()

        print("AUDIO: Priority {} unknown, couldn't play sound {}.".format(priority, sound))
        return -2, False

    def sort_channel_list(self):
        self.channel_list.sort(key=lambda x: self.play_time_dict[x])
