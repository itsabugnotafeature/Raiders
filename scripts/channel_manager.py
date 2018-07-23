import time


class ChannelManager:
    """
    Finds available channels to play sounds on.
    It uses priority and time to determine what should happen if there are no available channels
    """

    def __init__(self, **channel_lists):

        self.channel_name_dict = {}
        self.channel_access_time = {}

        for name, channel_list in channel_lists:
            self.channel_name_dict[name] = channel_list
            for channel in channel_list:
                self.channel_access_time[channel] = time.time()

    def associate(self, channel_list, name):

        self.channel_name_dict[name] = channel_list
